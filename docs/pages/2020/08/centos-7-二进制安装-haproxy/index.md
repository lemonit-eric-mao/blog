---
title: "CentOS 7 二进制安装 HAProxy"
date: "2020-08-12"
categories: 
  - "haproxy"
---

###### 禁用 **`SELinux`**

```ruby
setenforce 0
sed -i 's/^SELINUX=enforcing$/SELINUX=permissive/' /etc/selinux/config

```

###### 如果不禁用 **`SELinux`** ，程序启动时会抛出 `Starting proxy stats: cannot bind socket [0.0.0.0:1080]` 也可以执行如下命令来解决

```ruby
setsebool -P haproxy_connect_any=1
```

* * *

###### 添加 yum 源

```ruby
cat > /etc/yum.repos.d/ius-7.repo << ERIC

[ius]
name = IUS for Enterprise Linux 7 - \$basearch
baseurl = https://repo.ius.io/7/\$basearch/
enabled = 1
repo_gpgcheck = 0
gpgcheck = 1
gpgkey = https://repo.ius.io/RPM-GPG-KEY-IUS-7
[ius-debuginfo]
name = IUS for Enterprise Linux 7 - \$basearch - Debug
baseurl = https://repo.ius.io/7/\$basearch/debug/
enabled = 0
repo_gpgcheck = 0
gpgcheck = 1
gpgkey = https://repo.ius.io/RPM-GPG-KEY-IUS-7
[ius-source]
name = IUS for Enterprise Linux 7 - Source
baseurl = https://repo.ius.io/7/src/
enabled = 0
repo_gpgcheck = 0
gpgcheck = 1
gpgkey = https://repo.ius.io/RPM-GPG-KEY-IUS-7

ERIC

```

* * *

###### 查看

```ruby
# 更新源
yum makecache fast

# 查看
[root@k8s-master ~]# yum list | grep haproxy
haproxy.x86_64                            1.5.18-9.el7                   base
haproxy16u.x86_64                         1.6.15-1.el7.ius               ius
haproxy17u.x86_64                         1.7.12-1.el7.ius               ius
haproxy18u.x86_64                         1.8.25-1.el7.ius               ius
haproxy20.x86_64                          2.0.16-1.el7.ius               ius
haproxy22.x86_64                          2.2.1-1.el7.ius                ius
pcp-pmda-haproxy.x86_64                   4.3.2-7.el7_8                  updates
[root@k8s-master ~]#
```

* * *

###### 安装

```ruby
[root@k8s-master ~]# yum install -y haproxy22

[root@k8s-master ~]# haproxy -v
HA-Proxy version 2.2.1 2020/07/23 - https://haproxy.org/
Status: long-term supported branch - will stop receiving fixes around Q2 2025.
Known bugs: http://www.haproxy.org/bugs/bugs-2.2.1.html
Running on: Linux 5.8.0-1.el7.elrepo.x86_64 #1 SMP Sun Aug 2 18:18:16 EDT 2020 x86_64
[root@k8s-master deploy]#
```

* * *

###### 配置日志

```ruby
cat > /etc/rsyslog.d/haproxy.conf << ERIC
# 名称=[emerg, alert, crit, err, warning, notice, info, debug]
local2=debug     /var/log/haproxy.log

ERIC

# 重启rsyslog
systemctl restart rsyslog
```

* * *

###### 添加配置文件， 使用 k8s master 高可用配置来举例

```ruby
# 备份默认配置文件
mv /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg-bak

# 创建文件
cat > /etc/haproxy/haproxy.cfg << ERIC
global
  maxconn 10000                 # 最大同时10000连接
  daemon                        # 以daemon方式在后台运行

defaults
  log     127.0.0.1 local2      # local2 在 /etc/rsyslog.d/haproxy.conf 文件中配置
  # mode http                   # 默认的模式mode { tcp|http|health }，tcp是4层，http是7层，health只会返回OK
  retries         3             # 连接后端服务器失败重试次数，超过3次后会将失败的后端服务器标记为不可用。
  timeout client  1h            # 客户端响应超时             1小时
  timeout server  1h            # server端响应超时           1小时
  timeout connect 1h            # 连接server端超时           1小时
  timeout check   10s           # 对后端服务器的检测超时时间 10秒

listen stats                    # 定义监控页面
  mode  http
  bind  *:1080                  # Web界面的1080端口
  stats refresh 1s              # 每1秒更新监控数据
  stats uri /stats              # 访问监控页面的uri
  stats realm HAProxy\ Stats    # 监控页面的认证提示
  stats auth admin:654321       # 监控页面的用户名和密码

frontend kube_apiserver_front
  mode  tcp
  bind  *:6443                  # 监听6443端口
  default_backend kube_apiserver_back

backend kube_apiserver_back

  mode    tcp
  option  tcp-check
  balance roundrobin

  server kube-apiserver-1 192.168.20.91:6443 check inter 10s rise 3 fall 3 weight 1
  server kube-apiserver-2 192.168.20.92:6443 check inter 10s rise 3 fall 3 weight 1
  server kube-apiserver-3 192.168.20.93:6443 check inter 10s rise 3 fall 3 weight 1

ERIC

# 检查修改后的配置文件是否有效
haproxy -f /etc/haproxy/haproxy.cfg -c
```

* * *

###### 启动

```ruby
systemctl start haproxy && systemctl enable haproxy && systemctl status haproxy
```

* * *

* * *

* * *
