---
title: "secure ssh"
date: "2021-04-26"
categories: 
  - "运维"
---

# 适用于：CentOS 7.9

###### 创建脚本文件 `vim /root/secure_ssh.sh`

```bash
#!/bin/bash

# 参数化设置
DEFINE="5"                      # 定义登录失败次数的阈值
LOG_FILE="/var/log/secure"      # 安全日志文件路径
BLOCKED_IP_FILE="/etc/hosts.deny" # 被阻止IP地址的记录文件路径
LOG_TIMESTAMP=$(date +'%Y-%m-%d %H:%M:%S') # 获取当前时间戳

# 错误处理和日志记录函数
log_error() {
    local message=$1
    echo "[ERROR][$LOG_TIMESTAMP] $message" >&2
}

# IP地址格式验证函数
validate_ip() {
    local ip=$1
    # 使用正则表达式验证IP地址的格式
    if [[ ! $ip =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        log_error "Invalid IP address: $ip"
        return 1
    fi
    return 0
}

# 提取并阻止SSH失败登录次数超过阈值的IP地址
awk '/Failed/{print $(NF-3)}' "$LOG_FILE" | sort | uniq -c | while read count ip; do
    # 检查登录失败次数是否超过阈值
    if [ "$count" -ge "$DEFINE" ]; then
        # 验证IP地址格式
        if validate_ip "$ip"; then
            # 检查IP地址是否已经在hosts.deny中，若不在则添加
            if ! grep -q "$ip" "$BLOCKED_IP_FILE"; then
                echo "sshd:$ip:deny" >> "$BLOCKED_IP_FILE"
                echo "Blocked IP $ip due to $count failed login attempts."
            fi
        fi
    fi
done

```

* * *

* * *

* * *

# 适用于：Ubuntu 22.04

###### 创建脚本文件 `vim /root/secure_ssh.sh`

```bash
#!/bin/bash

# 定义日志文件路径
auth_log="/var/log/auth.log"

# 定义拉黑IP的阈值
failed_login_threshold=5
connection_closed_threshold=10

# 获取登录失败超过阈值的IP地址
failed_login_ips=$(grep 'Failed password' "$auth_log" | awk '{print $(NF-3)}' | sort | uniq -c | awk -v threshold="$failed_login_threshold" '$1 >= threshold {print $2}')

# 获取Connection closed by 不明IP地址的次数
connection_closed_ips=$(grep 'Connection closed by' "$auth_log" | grep -Eo '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' | sort | uniq -c | awk -v threshold="$connection_closed_threshold" '$1 >= threshold {print $2}')

# 合并拉黑IP列表
blacklist_ips=$(echo "$failed_login_ips"; echo "$connection_closed_ips")

# 检查是否有要拉黑的IP
if [ -n "$blacklist_ips" ]; then
    # 遍历每个IP
    for ip in $blacklist_ips; do
        # 检查是否已经存在于文件中
        if ! grep -q "^ALL: $ip$" /etc/hosts.deny; then
            echo "ALL: $ip" >> /etc/hosts.deny
            echo "Added $ip to /etc/hosts.deny"
        fi
    done
    # 重启相关服务以应用新的规则，例如SSH服务
    systemctl restart sshd
else
    echo "No IPs to blacklist"
fi

```

* * *

* * *

* * *

# 适用于：openEuler 22.03 SP4 系统

###### 创建脚本文件 `vim /root/secure_ssh.sh`

```bash
#!/bin/bash

# --- 配置区 ---
SET_NAME="blackhole"
TABLE_NAME="filter_ssh"
BLOCK_TIMEOUT="30d"        # 封禁时间：30天
FAILED_THRESHOLD=3         # 失败次数阈值
LOG_FILE="/var/log/secure"

# --- 1. 内核环境自动初始化 ---
# 检查表是否存在，不存在则创建全套拦截体系
if ! nft list table inet $TABLE_NAME &>/dev/null; then
    echo "正在初始化内核级防护框架..."
    # 创建表
    nft add table inet $TABLE_NAME
    # 创建集合（带自动过期功能）
    nft add set inet $TABLE_NAME $SET_NAME { type ipv4_addr\; flags timeout\; }
    # 创建输入链，优先级设为 -10 (在 firewalld 之前拦截)
    nft add chain inet $TABLE_NAME input { type filter hook input priority -10\; policy accept\; }
    # 添加拦截规则
    nft add rule inet $TABLE_NAME input ip saddr @$SET_NAME counter drop
    echo "初始化完成。"
fi

# --- 2. 提取白名单 ---
# 自动获取当前登录 IP，防止把自己封了
CURRENT_IP=$(who am i | awk '{print $NF}' | sed 's/[()]//g' | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b")
# 你也可以在这里手动添加固定白名单，例如 WHITELIST="1.1.1.1 2.2.2.2"
WHITELIST="127.0.0.1 $CURRENT_IP"

# --- 3. 扫描日志并执行封禁 ---
echo "正在扫描攻击源..."
BAD_IPS=$(grep -E "Failed password|authentication failure" "$LOG_FILE" \
    | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" \
    | sort | uniq -c \
    | awk -v t=$FAILED_THRESHOLD '$1>=t {print $2}')

for ip in $BAD_IPS; do
    # 白名单校验
    if [[ $WHITELIST =~ $ip ]]; then
        continue
    fi

    # 尝试将 IP 加入内核黑名单
    # 如果 IP 已存在，nft 会报错但没关系，我们重定向掉
    nft add element inet $TABLE_NAME $SET_NAME { $ip timeout $BLOCK_TIMEOUT } 2>/dev/null
    
    if [ $? -eq 0 ]; then
        echo "[$(date)] 成功封禁攻击者: $ip，有效期 $BLOCK_TIMEOUT" >> /var/log/ssh_shield.log
    fi
done

# --- 4. 统计信息 ---
COUNT=$(nft list set inet $TABLE_NAME $SET_NAME | grep -c "timeout")
echo "当前内核黑名单中共有 $COUNT 个活跃 IP。"
```

######
``` bash
# 将当前的内核规则导出为配置文件
nft list ruleset > /etc/nftables/ssh_shield.nft

# 修改 nftables 主配置文件，让它开机加载这个 shield 文件
# 如果文件不存在，可以直接创建
echo 'include "/etc/nftables/ssh_shield.nft"' > /etc/sysconfig/nftables.conf

# 设置服务自启动
systemctl enable nftables
```

###### 查看当前封禁列表：
``` bash
# 1. 先将命令别名化
alias banlist='nft list set inet filter_ssh blackhole'

# 2. 查看黑名单 IP
banlist
```

* * *

* * *

* * *

##### 添加定时任务，每分钟执行一次

```bash
crontab -e

*/1 * * * * /root/secure_ssh.sh
```

* * *

* * *

* * *
