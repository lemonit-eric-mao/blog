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

### ===== 基本配置 =====
LOG_FILE="/var/log/secure"
FAILED_THRESHOLD=5
BLOCK_DAYS=30
DROP_ZONE="drop"
DB_FILE="/root/ssh_block_db.txt"
LOG_RECORD="/root/ssh_block.log"

# 白名单（永不封禁）
WHITELIST=("127.0.0.1" "你的公网IP")

### ===== 自动检测当前登录IP加入白名单 =====
CURRENT_IP=$(who | awk '{print $5}' | sed 's/[()]//g')
WHITELIST+=("$CURRENT_IP")

### ===== 获取暴力破解IP =====
BAD_IPS=$(grep "Failed password" $LOG_FILE \
    | awk '{for(i=1;i<=NF;i++) if($i=="from") print $(i+1)}' \
    | sort | uniq -c \
    | awk -v t=$FAILED_THRESHOLD '$1>=t {print $2}')

NOW=$(date +%s)

for ip in $BAD_IPS
do
    # 跳过白名单
    if [[ " ${WHITELIST[@]} " =~ " ${ip} " ]]; then
        continue
    fi

    # 是否已存在
    firewall-cmd --zone=$DROP_ZONE --query-source=$ip &>/dev/null
    if [ $? -ne 0 ]; then
        firewall-cmd --permanent --zone=$DROP_ZONE --add-source=$ip
        echo "$ip $NOW" >> $DB_FILE
        echo "$(date) Blocked $ip" >> $LOG_RECORD
    fi
done

### ===== 清理过期IP =====
if [ -f $DB_FILE ]; then
    TMP_FILE="/tmp/ssh_block_tmp.txt"
    > $TMP_FILE
    while read ip timestamp
    do
        AGE=$(( (NOW - timestamp) / 86400 ))
        if [ $AGE -ge $BLOCK_DAYS ]; then
            firewall-cmd --permanent --zone=$DROP_ZONE --remove-source=$ip &>/dev/null
            echo "$(date) Unblocked $ip" >> $LOG_RECORD
        else
            echo "$ip $timestamp" >> $TMP_FILE
        fi
    done < $DB_FILE
    mv $TMP_FILE $DB_FILE
fi

firewall-cmd --reload &>/dev/null

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
