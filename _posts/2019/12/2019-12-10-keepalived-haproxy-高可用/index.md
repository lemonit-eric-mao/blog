---
title: "KeepAlived + HAProxy 高可用"
date: "2019-12-10"
categories: 
  - "keepalived"
---

##### 前置条件

[KeepAlived 安装部署-主节点](http://www.dev-share.top/2019/12/03/keepalived-%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2-%E4%B8%BB%E8%8A%82%E7%82%B9/ "KeepAlived 安装部署-主节点") [KeepAlived 安装部署-备节点](http://www.dev-share.top/2019/12/04/keepalived-%E5%AE%89%E8%A3%85%E9%83%A8%E7%BD%B2-%E5%A4%87%E8%8A%82%E7%82%B9/ "KeepAlived 安装部署-备节点") [使用HAProxy 为TiDB-Server 做负载均衡](http://www.dev-share.top/2019/09/25/%E4%BD%BF%E7%94%A8-docker-compose-%E5%81%9A-tidb-server-%E8%B4%9F%E8%BD%BD%E5%9D%87%E8%A1%A1-haproxy/ "使用HAProxy 为TiDB-Server 做负载均衡")

##### 只需要添加一段对HAProxy的监控脚本即可

###### 1 创建存放脚本的文件夹

```ruby
mkdir -p /etc/keepalived/scripts/
```

###### 2 创建脚本

```ruby
cat > /etc/keepalived/scripts/check_haproxy.sh << eric
#!/bin/bash
# 不要忘记给文件授权

# HAProxy 端口已经改为4600, 所以查看4600端口是否有进程来确认，HAProxy是否宕机
line=\$(netstat -lntp | grep 4600 | wc -l)
# 如果HAProxy已经宕机，将停止keepalived运行
if [ "\${line}" = "0" ]; then
     systemctl stop keepalived
fi

eric

```

###### 3 给脚本授权

```ruby
chmod -R 777 /etc/keepalived/scripts/check_haproxy.sh
```

###### 4 修改 KeepAlived 配置文件

```ruby
# 1 全局块
global_defs {
    # 这里的内容省略，使用的是之前文章中的配置
    ......
}

# 2 添加监控脚本(注意：脚本块，必须要在引用它的块的上面，这是有顺序的)
vrrp_script check_haproxy {
    script "/etc/keepalived/scripts/check_haproxy.sh"
    interval 1                                  # 调用脚本两次之间的间隔，默认为1秒
    weight 2                                    # 修改权重，默认是2
}

# 3 VRRP协议 实例块
vrrp_instance ERIC_VI_1 {

    # 这里的内容省略，使用的是之前文章中的配置
    ......

    interface ens160                            # 指定虚拟IP定义在那个网卡上面(本机指定为 ens160 网卡)
    # 定义虚拟IP块。客户通过该ip访问服务器
    virtual_ipaddress {
        172.160.180.168/24                      # 与指定的网卡是同一网段虚拟IP(使用ip add进行查看ens160 网卡的网段)
    }

    # 添加监控脚本
    track_script {                              # 执行监控nginx进程的脚本
        check_haproxy
    }
}

```
