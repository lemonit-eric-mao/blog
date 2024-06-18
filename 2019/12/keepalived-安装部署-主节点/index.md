---
title: "KeepAlived 安装部署-主节点"
date: "2019-12-03"
categories: 
  - "keepalived"
---

##### 概念

###### 一、 说到 Keepalived，需要先明确一点，这个 Keepalived 说的是`tcp的` 还是`http的`。

**1 tcp的Keepalived**   以检测web服务器为例，Keepalived从3个层次来检测服务器的状态 **（1）** IP层看网络是否正常Keepalived定期ping目标服务器，如果此IP地址没有激活，Keepalived便报告这台服务器失效，进行移除 **（2）** TCP层看web服务器端口是否正常例如一般web服务的端口为80，Keepalived定期查看80端口，如果没有启动，报告失效 **（3）** 应用层看应用程序是否正常Keepalived将根据用户的设定，检查服务器程序的运行是否正常，如果与用户的设定不相符，则Keepalived将把服务器从服务器群中剔除

**2 http的keep-alive**   http层有个keep-alive, 它主要是用于客户端告诉服务端，这个连接我还会继续使用，在使用完之后不要关闭。

- 在http早期，每个http请求都要求打开一个tpc socket连接，并且使用一次之后就断开这个tcp连接。
- 使用keep-alive可以改善这种状态，即在一次TCP连接中可以持续发送多份数据而不会断开连接。
- 通过使用keep-alive机制，可以减少tcp连接建立次数，也意味着可以减少TIME\_WAIT状态连接，以此提高性能和提高httpd服务器的吞吐率(更少的tcp连接意味着更少的系统内核调用,socket的accept()和close()调用)。
- 但是，keep-alive并不是免费的午餐,长时间的tcp连接容易导致系统资源无效占用。 配置不当的keep-alive，有时比重复利用连接带来的损失还更大。所以，正确地设置keep-alive timeout时间非常重要。
- **keep-alive timeout**   Httpd守护进程，一般都提供了keep-alive timeout时间设置参数。一个http产生的tcp连接在传送完最后一个响应后，需要等待keepalive\_timeout秒后，才开始关闭这个连接。

###### 二、 Keepalived 工作原理，TCP会在空闲了一定时间后发送数据给对方：

1. 如果主机可达，对方就会响应`ACK`应答，就认为是存活的。
2. 如果可达，但应用程序退出，对方就发`FIN`应答，发送TCP撤消连接。
3. 如果可达，但应用程序崩溃，对方就发`RST`消息。
4. 如果对方主机不响应`ACK、RST`，继续发送直到超时，撤消连接, 默认超时时间为2小时。

###### 三、对虚拟IP的理解？什么是虚拟IP？

  所谓的虚拟IP，其实就是一个**真实的IP**地址，只不过这个IP没有被任何主机使用，然后把这个**真实的IP**给**keepalived使用**, keepalived暂时把它想成是一个实现了 **`虚拟网卡`** 的技术, 我们需要虚拟网卡。

###### 四、Keepalived 集群工作思路

  在同一个集群中的 Keepalived，同时工作的只有一台机器，而其它节点都是备用状态，并不参加工作，只有当一台 Keepalived 死掉以后，其它的Keepalived会根据配置的规则选举出下一台接替工作的机器。

* * *

* * *

##### 环境

```ruby
[root@test1 ~]# keepalived -v
Keepalived v1.3.5 (03/19,2017)
```

| HostName | IP | DES |
| --- | --- | --- |
| test1 | 172.160.180.46 | master |
| test2 | 172.160.180.47 | node-1 |
| test3 | 172.160.180.48 | node-2 |
| test4 | 172.160.181.18 | node-3 |

###### 一、安装部署

```ruby
[root@test1 ~]# yum install -y keepalived
```

###### 二、配置文件

###### 查看当前要指定虚IP的网卡

```ruby
[root@test1 ~]# ip add show ens160
2: ens160: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    inet 172.160.180.46/24 brd 172.160.180.255 scope global noprefixroute ens160
[root@test1 ~]#
```

```ruby
cat > /etc/keepalived/keepalived.conf << eric


# 1 全局块
global_defs {
   # 接收邮件的邮箱列表
   notification_email {
     eric.mao@sinoeyes.com
   }
   notification_email_from eric@qq.com          # 发送邮件的人
   smtp_server smtp.exmail.qq.com               # smtp服务器地址
   smtp_connect_timeout 30                      # smtp超时时间
   router_id eric_keepalived_master             # 机器标识
   vrrp_skip_check_adv_addr
   vrrp_garp_interval 0
   vrrp_gna_interval 0
}

# 2 VRRP协议 实例块
vrrp_instance ERIC_VI_1 {                       # 定义一个vrrp的实例块，实例块的名称可以任意起，最好是字符串，这里我们定义的是 ERIC_VI_1
    nopreempt                                   # 设置 nopreempt 非抢占模式; (允许低优先级计算机保持主角色，即使高优先级计算机重新联机。如果保持抢占模式，只需要删除 nopreempt)
    state MASTER                                # 定义当前安装keepalived软件的服务器是 主节点(MASTER) 还是 备份节点(BACKUP)。只在抢占模式时起作用。
    virtual_router_id 56                        # 虚拟路由编号，主备要一致，范围是0-255
    priority 160                                # 优先级，谁的优先级高，谁更容易成为主节点， 数值越大级别越高
    advert_int 1                                # 主备服务器之间的通信间隔，单位是秒。
    # 服务器之间的认证方式
    authentication {
        auth_type PASS                          # 指定认证方式。PASS简单密码认证(推荐),AH:IPSEC认证(不推荐)。
        auth_pass 1111                          # 指定认证所使用的密码。最多8位。
    }
    interface ens160                            # 指定虚拟IP定义在那个网卡上面(本机指定为 ens160 网卡)
    # 定义虚拟IP块。客户通过该ip访问服务器
    virtual_ipaddress {
        172.160.180.168/24                      # 与指定的网卡是同一网段虚拟IP(使用ip add进行查看ens160 网卡的网段)
    }
}

eric

```

###### 三、启动

```ruby
[root@test1 ~]# systemctl start keepalived.service && systemctl enable keepalived.service && systemctl status keepalived.service
```

###### 四、查看是否创建成功

```ruby
[root@test1 ~]# ip add show ens160
2: ens160: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    inet 172.160.180.46/24 brd 172.160.180.255 scope global noprefixroute ens160
    # 发现多了一个虚拟IP就是成功了
    inet 172.160.180.168/24 scope global secondary ens160
[root@test1 ~]#

```

###### [备节点](http://www.dev-share.top/2019/12/04/keepalived-%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2-%E5%A4%87%E8%8A%82%E7%82%B9/ "备节点")

* * *

* * *

##### **`常见问题`**

###### 1 VRID 问题

```ruby
Dec  4 09:18:45 test1 Keepalived_vrrp[27680]: VRRP_Instance(ERIC_VI_1) ignoring received advertisment...
Dec  4 09:18:46 test1 Keepalived_vrrp[27680]: (ERIC_VI_1): ip address associated with VRID 51 not present in MASTER advert : 172.160.180.47
Dec  4 09:18:46 test1 Keepalived_vrrp[27680]: bogus VRRP packet received on ens160 !!!
# 原因
# virtual_router_id 51 有冲突
# 解决办法
# 修改配置文件中 virtual_router_id 的值 51 改为 56 或其它值
```

###### 2 虚拟IP 无法ping通

keepalived.conf 配置中默认 `vrrp_strict` 打开了，需要把它注释掉。重启keepalived即可ping通。
