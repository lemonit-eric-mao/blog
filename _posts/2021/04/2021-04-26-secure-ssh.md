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
SET_NAME="ssh_blacklist"       # ipset 集合名称
BLOCK_DAYS=30                  # 封禁天数
FAILED_THRESHOLD=3             # 失败次数阈值
LOG_FILE="/var/log/secure"     # 日志路径
WHITELIST_FILE="/root/ssh_whitelist.txt"
LOG_RECORD="/root/ssh_block.log"
DB_FILE="/root/ssh_block_db.txt" # 存储 IP 和 时间戳，用于过期清理

NOW=$(date +%s)

# 1. 环境初始化：检查 ipset 是否安装并创建集合
if ! command -v ipset &>/dev/null; then
    echo "正在安装 ipset..."
    dnf install ipset -y &>/dev/null
fi

# 创建 ipset 集合（如果不存在），timeout 0 表示由脚本手动控制清理
ipset list $SET_NAME &>/dev/null
if [ $? -ne 0 ]; then
    ipset create $SET_NAME hash:ip hashsize 4096 maxelem 65536
    # 将 ipset 关联到 firewalld 的 drop 区域
    firewall-cmd --permanent --zone=drop --add-source=ipset:$SET_NAME
    firewall-cmd --reload &>/dev/null
fi

# 2. 读取白名单
WHITELIST=()
if [ -f "$WHITELIST_FILE" ]; then
    while read -r line; do
        [[ "$line" =~ ^#.*$ || -z "$line" ]] && continue
        WHITELIST+=("$line")
    done < "$WHITELIST_FILE"
fi

# 自动加入当前登录 IP (防止误封自己)
CURRENT_IP=$(who am i | awk '{print $NF}' | sed 's/[()]//g')
if [[ $CURRENT_IP =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    WHITELIST+=("$CURRENT_IP")
fi

# 3. 提取失败 IP
# 兼容 "Failed password" 和 "authentication failure" 两种日志格式
BAD_IPS=$(grep -E "Failed password|authentication failure" "$LOG_FILE" \
    | grep -oE "\b([0-9]{1,3}\.){3}[0-9]{1,3}\b" \
    | sort | uniq -c \
    | awk -v t=$FAILED_THRESHOLD '$1>=t {print $2}')

# 4. 白名单判断函数 (支持网段)
is_whitelisted() {
    local ip=$1
    for wip in "${WHITELIST[@]}"; do
        if [[ "$wip" == */* ]]; then
            # 如果是网段，使用 ipcalc 验证
            if command -v ipcalc &>/dev/null; then
                ipcalc -c "$ip" "$wip" &>/dev/null && return 0
            fi
        else
            [[ "$ip" == "$wip" ]] && return 0
        fi
    done
    return 1
}

# 5. 执行封禁逻辑
for ip in $BAD_IPS; do
    is_whitelisted "$ip" && continue

    # 检查 ipset 中是否已存在
    ipset test $SET_NAME "$ip" &>/dev/null
    if [ $? -ne 0 ]; then
        ipset add $SET_NAME "$ip"
        # 记录到数据库文件供过期清理
        echo "$ip $NOW" >> "$DB_FILE"
        echo "$(date '+%Y-%m-%d %H:%M:%S') Blocked $ip" >> "$LOG_RECORD"
    fi
done

# 6. 过期清理逻辑
if [ -f "$DB_FILE" ]; then
    TMP_FILE=$(mktemp)
    while read -r ip timestamp; do
        AGE=$(( (NOW - timestamp) / 86400 ))
        if [ "$AGE" -ge "$BLOCK_DAYS" ]; then
            ipset del $SET_NAME "$ip" &>/dev/null
            echo "$(date '+%Y-%m-%d %H:%M:%S') Unblocked $ip (Expired)" >> "$LOG_RECORD"
        else
            echo "$ip $timestamp" >> "$TMP_FILE"
        fi
    done < "$DB_FILE"
    mv "$TMP_FILE" "$DB_FILE"
fi

exit 0
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
