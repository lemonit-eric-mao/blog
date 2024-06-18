---
title: 'secure ssh'
date: '2021-04-26T04:29:16+00:00'
status: private
permalink: /2021/04/26/secure-ssh
author: 毛巳煜
excerpt: ''
type: post
id: 7174
category:
    - 运维
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
适用于：CentOS 7.9
==============

###### 创建脚本文件 `vim /root/secure_ssh.sh`

```bash
#!/bin/bash

# 参数化设置
DEFINE="5"                      # 定义登录失败次数的阈值
LOG_FILE="/var/log/secure"      # 安全日志文件路径
BLOCKED_IP_FILE="/etc/hosts.deny" # 被阻止IP地址的记录文件路径
LOG_TIMESTAMP=<span class="katex math inline">(date +'%Y-%m-%d %H:%M:%S') # 获取当前时间戳

# 错误处理和日志记录函数
log_error() {
    local message=</span>1
    echo "[ERROR][<span class="katex math inline">LOG_TIMESTAMP]</span>message" >&2
}

# IP地址格式验证函数
validate_ip() {
    local ip=<span class="katex math inline">1
    # 使用正则表达式验证IP地址的格式
    if [[ !</span>ip =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+<span class="katex math inline">]]; then
        log_error "Invalid IP address:</span>ip"
        return 1
    fi
    return 0
}

# 提取并阻止SSH失败登录次数超过阈值的IP地址
awk '/Failed/{print <span class="katex math inline">(NF-3)}' "</span>LOG_FILE" | sort | uniq -c | while read count ip; do
    # 检查登录失败次数是否超过阈值
    if [ "<span class="katex math inline">count" -ge "</span>DEFINE" ]; then
        # 验证IP地址格式
        if validate_ip "<span class="katex math inline">ip"; then
            # 检查IP地址是否已经在hosts.deny中，若不在则添加
            if ! grep -q "</span>ip" "<span class="katex math inline">BLOCKED_IP_FILE"; then
                echo "sshd:</span>ip:deny" >> "<span class="katex math inline">BLOCKED_IP_FILE"
                echo "Blocked IP</span>ip due to $count failed login attempts."
            fi
        fi
    fi
done


```

- - - - - -

- - - - - -

- - - - - -

适用于：Ubuntu 22.04
================

###### 创建脚本文件 `vim /root/secure_ssh.sh`

```bash
#!/bin/bash

# 定义日志文件路径
auth_log="/var/log/auth.log"

# 定义拉黑IP的阈值
failed_login_threshold=5
connection_closed_threshold=10

# 获取登录失败超过阈值的IP地址
failed_login_ips=<span class="katex math inline">(grep 'Failed password' "</span>auth_log" | awk '{print <span class="katex math inline">(NF-3)}' | sort | uniq -c | awk -v threshold="</span>failed_login_threshold" '<span class="katex math inline">1 >= threshold {print</span>2}')

# 获取Connection closed by 不明IP地址的次数
connection_closed_ips=<span class="katex math inline">(grep 'Connection closed by' "</span>auth_log" | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | sort | uniq -c | awk -v threshold="<span class="katex math inline">connection_closed_threshold" '</span>1 >= threshold {print <span class="katex math inline">2}')

# 合并拉黑IP列表
blacklist_ips=</span>(echo "<span class="katex math inline">failed_login_ips"; echo "</span>connection_closed_ips")

# 检查是否有要拉黑的IP
if [ -n "<span class="katex math inline">blacklist_ips" ]; then
    # 遍历每个IP
    for ip in</span>blacklist_ips; do
        # 检查是否已经存在于文件中
        if ! grep -q "^ALL: <span class="katex math inline">ip</span>" /etc/hosts.deny; then
            echo "ALL: <span class="katex math inline">ip" >> /etc/hosts.deny
            echo "Added</span>ip to /etc/hosts.deny"
        fi
    done
    # 重启相关服务以应用新的规则，例如SSH服务
    systemctl restart sshd
else
    echo "No IPs to blacklist"
fi


```

- - - - - -

- - - - - -

- - - - - -

##### 添加定时任务，每分钟执行一次

```ruby
crontab -e

*/1 * * * * /root/secure_ssh.sh

```

- - - - - -

- - - - - -

- - - - - -