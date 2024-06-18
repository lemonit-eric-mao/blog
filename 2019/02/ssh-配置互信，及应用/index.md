---
title: "SSH 配置互信，及应用"
date: "2019-02-22"
categories: 
  - "linux服务器"
---

#### 手工配置 ssh 互信及 sudo 免密码

##### 登录主控机配置好 sudo 免密码

###### 配置sudo免密码 分步命令：

```ruby
[root@shared-server ~]# useradd mao_siyu_test
[root@shared-server ~]# passwd mao_siyu_test
[root@shared-server ~]# echo "mao_siyu ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
# 查看是否追加成功，当然这个命令也可以手动添加权限
[root@shared-server ~]# visudo
```

###### 配置sudo免密码 命令简写

```ruby
[root@shared-server ~]# useradd mao_siyu_test && passwd mao_siyu_test
passwd: all authentication tokens updated successfully.
[root@shared-server ~]#
[root@shared-server ~]# echo "mao_siyu ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers && visudo
```

###### 配置 SSH互信

`ssh-copy-id -i 指定本地公钥文件 远程目标机器IP` `ssh-copy-id 将本地 ~/.ssh/id_rsa.pub 写到远程机器的 ~/.ssh/authorized_key.文件中`

```ruby
[root@shared-server ~]# ssh-keygen -t rsa
[root@shared-server ~]#
[root@shared-server ~]# ssh-copy-id -i ~/.ssh/id_rsa.pub 172.16.26.36
[root@shared-server ~]#
[root@shared-server ~]# ssh 172.16.26.36 或者机器名
```

##### 在主控机，向多台服务器发送指令 （前题建产好SSH互信）

`同时为 172.16.26.56 与 172.16.26.66安装 vim软件`

```ruby
[root@shared-server ~]# ssh 172.16.26.56 sudo -su root yum install -y vim &&  ssh 172.16.26.66
```

##### shell 脚本定义变量的写法

```ruby
[root@shared-server ~]# command="cat /etc/redhat-release"
[root@shared-server ~]# ssh 172.16.26.56 sudo -su root $command &&  ssh 172.16.26.66 sudo -su root $command
```

* * *

**通常情况下配置 ssh互信是 主控机 root账户 与 节点机 root账户建立ssh互信;** **但也会有另一种情况，就是主控机的非 root账户 与 节点机的 root账户建立互信等情况如下**

| 主控机账户 | 节点机账户 | 配置ssh互信 |
| --- | --- | --- |
| root | root | ssh-copy-id -i ~/.ssh/id\_rsa.pub 节点机IP |
| gitlab-runner | root | ssh-copy-id -i ~/.ssh/id\_rsa.pub root@节点机IP |
| tidb | tidb | ssh-copy-id -i ~/.ssh/id\_rsa.pub 节点机IP |

* * *

* * *

* * *

* * *

* * *

* * *

##### 常见问题

##### `WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!`

```ruby
Failed to connect to the host via ssh: @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@    WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED!     @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
The fingerprint for the ECDSA key sent by the remote host is
SHA256:kDy4BKa7GfqJb8ejuR+oCoaRhBAS8neskjvas05e2Bc.
Please contact your system administrator.
Add correct host key in /root/.ssh/known_hosts to get rid of this message.
Offending ECDSA key in /root/.ssh/known_hosts:25       # 这里明确指出，/root/.ssh/known_hosts 文件的第25行的密钥错误
Password authentication is disabled to avoid man-in-the-middle attacks.
Keyboard-interactive authentication is disabled to avoid man-in-the-middle attacks.
Permission denied (publickey,password).
```

###### 解决办法

**删除`/root/.ssh/known_hosts`文件，重建立SSH互信**

* * *

* * *

* * *

###### `Failed to connect to the host via ssh: ssh: connect to host 10.22.12.59 port 22: Connection timed out`

**这个问题非常简单，目标服务器连接失败，要在目标服务器上排查原因**

* * *

* * *

* * *

###### 远程22端口变更时，操作方法

```ruby
ssh -p 11016 -i ~/.ssh/id_rsa.pub root@44.96.155.38
```

* * *

* * *

* * *

###### ssh强制忽略Host检查

**问题：`Are you sure you want to continue connecting (yes/no/[fingerprint])?`**

```ruby
ssh -o StrictHostKeyChecking=no root@44.96.155.38
```

* * *

* * *

* * *
