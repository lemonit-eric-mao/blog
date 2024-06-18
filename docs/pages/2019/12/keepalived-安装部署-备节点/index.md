---
title: "KeepAlived 安装部署-备节点"
date: "2019-12-04"
categories: 
  - "keepalived"
---

###### [主节点安装](http://www.dev-share.top/2019/12/03/keepalived-%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2-%E4%B8%BB%E8%8A%82%E7%82%B9/ "主节点安装")

##### 环境

```ruby
[root@test2 ~]# keepalived -v
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
[root@test2 ~]# yum install -y keepalived
```

###### 二、配置文件

###### 查看当前要指定虚IP的网卡

```ruby
[root@test2 ~]# ip add show ens160
2: ens160: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    inet 172.160.180.47/24 brd 172.160.180.255 scope global noprefixroute ens160
[root@test2 ~]#
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
   router_id eric_keepalived_node_1             # 机器标识
   vrrp_skip_check_adv_addr
   vrrp_garp_interval 0
   vrrp_gna_interval 0
}

# 2 VRRP协议 实例块
vrrp_instance ERIC_VI_1 {                       # 定义一个vrrp的实例块，实例块的名称可以任意起，最好是字符串，这里我们定义的是 ERIC_VI_1
    nopreempt                                   # 设置 nopreempt 非抢占模式; (允许低优先级计算机保持主角色，即使高优先级计算机重新联机。如果保持抢占模式，只需要删除 nopreempt)
    state BACKUP                                # 定义当前安装keepalived软件的服务器是 主节点(MASTER) 还是 备份节点(BACKUP)。只在抢占模式时起作用。
    virtual_router_id 56                        # 虚拟路由编号，主备要一致，范围是0-255
    priority 100                                # 优先级，谁的优先级高，谁更容易成为主节点， 数值越大级别越高
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
[root@test2 ~]# systemctl start keepalived.service && systemctl enable keepalived.service && systemctl status keepalived.service
```

###### 四、查看是否创建成功

**备节点与主节点不同，需要停掉主节点，备节点才可以查到虚拟IP；** **由此可见**，`KeepAlived 高可用是通过动态切换生成虚拟IP地址来达到的高可用！`

```ruby
[root@test2 ~]# ip addr show ens160
2: ens160: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    inet 172.160.180.47/24 brd 172.160.180.255 scope global noprefixroute ens160
    # 发现多了一个虚拟IP就是成功了
    inet 172.160.180.168/24 scope global secondary ens160
[root@test2 ~]#

```
