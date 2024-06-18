---
title: '了解学习 Linux 操作系统'
date: '2023-01-08T04:17:51+00:00'
status: private
permalink: /2023/01/08/%e4%ba%86%e8%a7%a3%e5%ad%a6%e4%b9%a0-linux-%e6%93%8d%e4%bd%9c%e7%b3%bb%e7%bb%9f
author: 毛巳煜
excerpt: ''
type: post
id: 9636
category:
    - 自学整理
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
CentOS 系统的启动流程
--------------

[![](http://qiniu.dev-share.top/image/linux/file-permission-images/01.png)](http://qiniu.dev-share.top/image/linux/file-permission-images/01.png)

Linux 系统文件的基本属性
---------------

- [![](http://qiniu.dev-share.top/image/linux/file-permission-images/02.png)](http://qiniu.dev-share.top/image/linux/file-permission-images/02.png)

### 第一列 它有11个字符

- 第1个字符 表示文件的类型 
  - 首字母【d】开头 `d---------.` 表示的是一个文件 文件夹
  - 首字母【-】开头 `----------.` 表示的是一个文件 普通文件
  - 首字母【l】开头 `l---------.` 表示的是一个文件 链接文件
  - 首字母【c】开头 `c---------.` 表示的是一个文件 串口设备
  - 首字母【b】开头 `b---------.` 表示的是一个文件 存储设备
- 第2 ~ 10字符 操作权限 
  - rwx，读写执行，421 
      - `r` 读 4
      - `w` 写 2
      - `x` 执 1
      - `-` 无 0
  - 3个一组 
      - 一组：第【2 ~ 4】字符 `-rwx------.` 属主权限(文件/文件夹，的创建者，他自己有哪些操作权限)
      - 二组：第【5 ~ 7】字符 `----rwx---.` 属组权限(文件/文件夹，所属群组中，所有人都有哪些操作权限)
      - 三组：第【8 ~ 10】字符 `-------rwx.` 其它权限(文件/文件夹，)
- 最后一个字符(第11位) `.` 的作用 
  - 这个点表示的是存在`SELinux的安全标签`
      - 我们用`getenforce`来查看`SELinux`的运行模式
      - ```shell
            [root@eric-mao (14:10:45) ~]# getenforce
            Enforcing
            
            ```
  - `/etc/selinux`
  - ```shell
      ## 查看
      [root@eric-mao (14:11:55) ~]# cat /etc/selinux/config
      
      # This file controls the state of SELinux on the system.
      # SELINUX= can take one of these three values:
      #     enforcing - SELinux security policy is enforced.
      #     permissive - SELinux prints warnings instead of enforcing.
      #     disabled - No SELinux policy is loaded.
      SELINUX=enforcing
      # SELINUXTYPE= can take one of three values:
      #     targeted - Targeted processes are protected,
      #     minimum - Modification of targeted policy. Only selected processes are protected.
      #     mls - Multi Level Security protection.
      SELINUXTYPE=targeted
      
      
      ```
      
      
      - 改为禁用
            
            
            - ```shell
                    sed -i s/SELINUX=enforcing/SELINUX=disabled/g /etc/selinux/config
                    
                    ```
                    
                    
                    - 需要重启系统后才生效
      - 改为启用 
            - ```shell
                    sed -i s/SELINUX=disabled/SELINUX=enforcing/g /etc/selinux/config
                    
                    ```
                    
                    
                    - 需要重启系统后才生效

#### 测试

- 在开启`SELinux`时创建文件 
  - ```shell
      ## 查看 SELinux 的运行模式
      [root@eric-mao (14:10:45) ~]# getenforce
      Enforcing
      
      [root@eric-mao (14:13:19) ~]# touch test1-Enforcing.log
      
      
      ```
- 在关闭`SELinux`时创建文件 
  - ```shell
      ## 查看 SELinux 的运行模式
      [root@eric-mao (14:17:15) ~]# getenforce
      Disabled
      
      [root@eric-mao (14:17:21) ~]# touch test1-Disabled.log
      
      
      ```
- 查看两个文件的安全上下文是什么样的 
  - ```shell
      [root@eric-mao (14:20:13) ~]# ll -Z
      -rw-r--r--. root root unconfined_u:object_r:admin_home_t:s0    test1-Enforcing.log
      -rw-r--r--  root root ?                                        test1-Disabled.log
      
      ```
  - > **关掉了`SELinux`，创建的文件就`没有了这个安全上下文`了，也就没有了这个点`.`了**
- 最后在重新开启`SELinux`，再次查看，发现文件的点`.`又会自动加回来了，只是`安全上下文变的不一样了`
  - ```shell
      [root@eric-mao (14:24:09) ~]# ll -Z
      -rw-r--r--. root root unconfined_u:object_r:admin_home_t:s0    test1-Enforcing.log
      -rw-r--r--. root root system_u:object_r:admin_home_t:s0        test1-Disabled.log
      
      
      ```

### 第二列

### 第三列

文件权限
----

### 隐藏权限

- > 隐藏权限是从`CentOS 6`以后才有的
- `chattr` **change attribute**
- `lsattr`
  
  
  - `lsattr filename` 查看文件权限
  - `lsattr -d dirname` 查看目录权限

#### **不可修改权限**

- > 1. **无论任何人，如果需要修改需要先删除`i`权限**
  > 2. 查看文件是否设置了`i`权限用 **`lsattr filename`**
- **命令 `chattr +i filename` `chattr -i filename`**
  - [![](http://qiniu.dev-share.top/image/linux/file-permission-images/08.png)](http://qiniu.dev-share.top/image/linux/file-permission-images/08.png)

#### **只追加权限**

- > 1. 对于日志系统很好用，这个权限让目标文件只能追加，不能删除，而且不能通过编辑器追加。
  > 2. 如果需要修改需要先删除`a`权限
  > 3. 查看文件是否设置了`a`权限用 **`lsattr filename`**
- 命令 `chattr +a filename` `chattr -a filename`
  
  
  - [![](http://qiniu.dev-share.top/image/linux/file-permission-images/09.png)](http://qiniu.dev-share.top/image/linux/file-permission-images/09.png)

### 特殊权限

#### **s权限（SetUID）**

- > - **SetUID：**
  >     - `SetUID`，简称 `SUID`
  >     - `s权限`是让普通用户，能够以root用户的角色运行，只有root帐号才能运行的程序或命令。
  > - **s：**
  >     - 文件属主和组设置SUID和GUID，文件在被设置了s权限后将以root身份执行。
  > - **在设置s权限时文件属主、属组必须先设置相应的x权限，否则s权限并不能正真生效。**
  > - `chmod 4755 filename`
  > - `chmod +s filename` 属主与属组，都加上`s`权限
  > - `chmod u+s filename` 属主，加上`s`权限
  > - `chmod g+s filename` 属组，加上`s`权限
  > - `chmod -s filename` 删除`s`权限
- **命令 `chmod +s filename` `chmod -s filename`**
  - [![](http://qiniu.dev-share.top/image/linux/file-permission-images/03.png)](http://qiniu.dev-share.top/image/linux/file-permission-images/03.png)
  - 查看结果：未设置相应的`x`权限，结果以大`S`显示
  - [![](http://qiniu.dev-share.top/image/linux/file-permission-images/04.png)](http://qiniu.dev-share.top/image/linux/file-permission-images/04.png)
  - 查看结果：设置相应的`x`权限，结果以小`s`显示
  - [![](http://qiniu.dev-share.top/image/linux/file-permission-images/05.png)](http://qiniu.dev-share.top/image/linux/file-permission-images/05.png)

#### **粘滞位（stick bit）**

- > **防止普通用户删除或移动其他用户的文件**
  > 
  > 
  > - **stick bit：**
  >     - `stick bit`，简称 `sbit`
  > - 设置粘滞位的文件，只能由以下账户删除 
  >     1. 超级管理员
  >     2. 该目录的所有者
  >     3. 该文件的所有者
  > - `chmod +t filename`
  > - `chmod o+t filename`
- **命令 `chmod +t filename` `chmod -t filename`**
  - [![](http://qiniu.dev-share.top/image/linux/file-permission-images/06.png)](http://qiniu.dev-share.top/image/linux/file-permission-images/06.png)
  - 查看结果：同样的，当没有`x`权限的时候，为大写`T`
  - [![](http://qiniu.dev-share.top/image/linux/file-permission-images/07.png)](http://qiniu.dev-share.top/image/linux/file-permission-images/07.png)

#### `su 和 sudo`

- `/etc/sudoers`

### ACL权限

- > 文件的`ACL`权限，提供了所有者(属主 属组 其他人)的读、写、执行权限之外的特殊权限控制
- **设置的对象**
  - 文件
  - 目录
- 受益的对象 
  - 用户
  - 群组 
      - 群组中的成员
- 查看`ACL`的权限 
  - `getfacl finename`
  - ```shell
      [root@eric-mao (10:14:17) ~]# getfacl passfile
      # file: passfile
      # owner: root
      # group: root
      user::rw-
      group::r--
      other::r--
      
      
      ```
- 设定`ACL`的权限
  
  
  - `setfacl` 它实际上是通过掩码来操作的
  - ```shell
      
      ```
  - `mask` 最大有效权限(这儿会涉及到，十进制、二进制的转换)
      
      
      - 按位与操作
      - rwx 421
- 删除`ACL`的权限 
  - `setfacl -x u:用户名 文件名` 删除指定用户的ACL权限
  - `setfacl -x g:用户组名 文件名` 删除指定用户组的ACL权限
- 递归`ACL`的权限 
  - `setfacl -m u:用户名:权限 -R 文件名` 设定当前目录以及所有子目录，为相同的权限
- 默认`ACL`的权限 
  - `setfacl -m d:u:用户名:权限 文件名` 创建目录时的默认权限，所有子目录会默认继承父权限

字符集
---

- ```shell
  [root@eric-mao (16:58:35) ~]# echo $LANG
  en_US.UTF-8
  
  ## 也可以这样做
  [root@eric-mao (16:58:39) ~]# cat /etc/locale.conf
  LANG="en_US.UTF-8"
  
  ## 还可以这样做
  [root@eric-mao (16:58:39) ~]# localectl set-locale LANG=en_US.UTF-8
  
  
  ```

特殊符号
----

### 表示位置的

1. `/` 系统根目录
2. `~` `飘号` 当前用户主目录
3. `.` 当前目录
4. `..` 上一级目录
5. `-` 切换到上一次目录

### 引号相关

1. `''` **单引号** 字符串`常`量 里面的内容是什么，输出的就是什么
2. `""` **双引号** 字符串`变`量 里面的内容可以是动态的
3. ``` ` \*\*反引号\*\* 命令替换
4. `\` **反斜杠** 转义字符

### 重定向

- 重定向输入 
  - `   标准输入，`覆盖`输入<ul><li>2</li><li><p>分析：</p><ul><li>标准输入 0</li><li>标准输出 1</li><li>标准错误 2</li></ul></li><li><blockquote><p>  解释：同时把错误信息或正确信息都记录到文件中</p></blockquote></li></ul>`
  - `  标准输入，`追加`输入`
- 重定向输出
  
  
  - `>` 标准输出，`覆盖`写入
  - `>>` 标准输出，`追加`写入

### 管道符 `|`

- > **什么是`管道`和`管道符`？**
  > 
  >  `管道`和`管道符`，它俩是两个概念
  > 
  > 
  > 1. **`管道`**，它是在Unix编程里面，有一个叫做`IPC进程间通信`的技术 
  >     - 它会为`有名管道`、`匿名管道`用来实现`跨进程间的通信`
  > 2. **`管道符`**，它是一个符号 
  >     - **作用**：把前面一个命令的结果，通过管道符传递给后面的命令。后面的命令把结果在次进行处理。
  >     - **注意**：`管道`默认传递的是文字符号。
- 例如：`cat /etc/shadow | wc -l`查看`shadow`文件内容，一共有多少行

### 其它字符

- `#` 它通常出现在哪些地方？ 
  - 终端 `[root@eric-mao (10:50:59) ~]#`表示你是root用户
  - `*.conf` 配置文件中 表示注释
- `$` 它通常出现在哪些地方？ 
  - 终端 `[maosiyu@eric-mao (10:50:59) ~]$` 表示你是普通用户
  - 脚本或配置文件中 `$LANG`， 它是一个变量
- `&` 它通常出现在哪些地方？ 
  - 终端 将它放在命令的最后，表示在后台运行
- `;`
  - 编程中 命令或语句的结束
  - 脚本命令 连续不同命令的分隔符
- `!`
  - 终端 `!ls` 执行上一次执行的`ls`开头的命令
  - vim 文本编辑器 强制

`find` 命令常见用法
-------------

- 查找2天内被`访问`的文件 根目录下 
  - `find / -atime -2`
- 查找6天内被`修改`的文件 根目录下 
  - `find / -mtime -6`
- 查找6天内被`修改`的文件 根目录下 指定扩展名为 `*.log`
  - `find / -mtime -6 -name '*.log'`
- 查找6天内被`修改`的文件 根目录下 权限是 `644`的 
  - `find / -mtime -6 -perm 644`
- 查找当前目录下所有的子目录 
  - `find . -type d`
- 查找当前目录下所有的子目录，指定查找层数 
  - `find . -maxdepth 3 -type d`
- 查找当前目录下所有的文件 
  - `find . ! -type d`或者`find . -type f`
- 查找当前目录下所有的文件，指定查找层数 
  - `find . -maxdepth 3 -type f`
- 查找当前目录下，大小`200M`的文件 
  - `find . -size +200M`
- 查找当前目录下所有的文件，指定查找层数，并且让文件以 长格式显示 
  - `find . -maxdepth 3 -type f -ls`

定时任务
----

- **定时任务**
- **端口保活**
- **业务-低谷期 凌晨`5 ~ 6`点**
- `crond` 它是Linux系统中，后台运行的服务软件，`crontab`中的定时任务，就是由它来执行的，它是以`分钟级`执行的
  
  
  - 如果有需求想精确到`秒级`我们可以使用脚本中的`sleep()`函数
- **确认定时服务是否安装**
  - ```shell
      [root@eric-mao (15:51:36) ~]# rpm -aq cronie
      cronie-1.4.11-19.el7.x86_64
      
      ```
- **查看安装信息**
  - ```shell
      [root@eric-mao (15:51:57) ~]# rpm -ql cronie
      /etc/cron.d
      /etc/cron.d/0hourly
      /etc/cron.deny
      /etc/pam.d/crond
      /etc/sysconfig/crond
      /usr/bin/crontab
      /usr/lib/systemd/system/crond.service
      /usr/sbin/crond
      /usr/share/doc/cronie-1.4.11
      /usr/share/doc/cronie-1.4.11/AUTHORS
      /usr/share/doc/cronie-1.4.11/COPYING
      /usr/share/doc/cronie-1.4.11/ChangeLog
      /usr/share/doc/cronie-1.4.11/INSTALL
      /usr/share/doc/cronie-1.4.11/README
      /usr/share/man/man1/crontab.1.gz
      /usr/share/man/man5/crontab.5.gz
      /usr/share/man/man8/cron.8.gz
      /usr/share/man/man8/crond.8.gz
      /var/spool/cron
      
      ```
- **定时任务的种类**
  1. `crond`服务 **`最常见的`**
  2. `atd`服务 它是临时的，运行一次就结束了
  3. `anacron`服务 它的要求是，非`7*24小时`运行的服务器上
- **定时任务分类**
  - **系统定时任务**
      - `crontab` 定时任务配置文件 
            - `crontab -l` 查看定时任务
            - `crontab -e` 编辑定时任务
            - `crontab -r` 删除定时任务
            - `crontab -i` 删除定时任务，删除前提示
            - `crontab -u` 指定用户定时任务列表
            - ```shell
                    [root@eric-mao (16:32:42) ~]# cat /etc/crontab
                    SHELL=/bin/bash
                    PATH=/sbin:/bin:/usr/sbin:/usr/bin
                    MAILTO=root
                    
                    # For details see man 4 crontabs
                    
                    # Example of job definition:
                    # .---------------- minute (0 - 59)
                    # |  .------------- hour (0 - 23)
                    # |  |  .---------- day of month (1 - 31)
                    # |  |  |  .------- month (1 - 12) OR jan,feb,mar,apr ...
                    # |  |  |  |  .---- day of week (0 - 6) (Sunday=0 or 7) OR sun,mon,tue,wed,thu,fri,sat
                    # |  |  |  |  |
                    # *  *  *  *  * user-name  command to be executed
                    
                    
                    ```
  - 使用 `系统定时任务+logrotate` 来实现系统日志的分割，效果如下
      
      
      - ```shell
            [root@eric-mao (16:17:05) ~]# find /var/log/ -type f -name cron*
            /var/log/cron-20221218
            /var/log/cron-20221225
            /var/log/cron-20230101
            /var/log/cron-20230108
            /var/log/cron
            
            ```
  - **用户定时任务**

- - - - - -

**`sudo su -` 相关命令**
====================

<table><thead><tr><th>命令/选项</th><th>描述</th><th>示例</th></tr></thead><tbody><tr><td>`sudo su -`</td><td>以超级用户权限切换到新用户，并加载其环境</td><td>`sudo su - username`</td></tr><tr><td>`sudo su`</td><td>以超级用户权限切换到新用户，不加载其环境</td><td>`sudo su username`</td></tr><tr><td>`su`</td><td>切换到新用户，通常需要提供目标用户的密码</td><td>`su username`</td></tr><tr><td>`su -`</td><td>以新用户登录，加载其环境</td><td>`su - username`</td></tr><tr><td>`sudo -s`</td><td>以超级用户权限启动新shell，不加载新用户的环境</td><td>`sudo -s`</td></tr><tr><td>`sudo -i`</td><td>以超级用户权限启动新shell，加载新用户的环境</td><td>`sudo -i`</td></tr><tr><td>`sudo -u username command`</td><td>以指定用户的身份执行命令</td><td>`sudo -u username command`</td></tr><tr><td>`sudo -l`</td><td>列出当前用户的sudo权限</td><td>`sudo -l`</td></tr><tr><td>`sudo -k`</td><td>使sudo超时，需要重新验证密码</td><td>`sudo -k`</td></tr><tr><td>`su -c command username`</td><td>以指定用户身份执行命令</td><td>`su -c command username`</td></tr><tr><td>`su -l username`</td><td>以指定用户的身份登录，加载其环境</td><td>`su -l username`</td></tr><tr><td>`login username`</td><td>登录到另一个用户帐户，通常需要提供密码</td><td>`login username`</td></tr><tr><td>`shell -c command`</td><td>在shell中运行指定的命令</td><td>`bash -c "command"`</td></tr><tr><td>`shell -l`</td><td>启动一个登录shell，加载用户的环境变量</td><td>`bash -l`</td></tr><tr><td>`shell -s shell`</td><td>指定要使用的shell</td><td>`bash -s /bin/bash`</td></tr><tr><td>`sudo -E`</td><td>保留环境变量，不使用sudo默认的环境</td><td>`sudo -E`</td></tr><tr><td>`sudo -H`</td><td>使用目标用户的家目录</td><td>`sudo -H`</td></tr><tr><td>`sudo -u username -i`</td><td>以指定用户的身份登录，加载其环境</td><td>`sudo -u username -i`</td></tr></tbody></table>