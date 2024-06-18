---
title: "SCP 迁移docker镜像，自动填写密码"
date: "2019-11-19"
categories: 
  - "shell"
---

##### 前置条件

- 需要安装 **`yum install -y expect`**
- **`spawn`** ：后面跟具体要执行的命令
- **`expect`** ：定义字符内容用于匹配上面spawn后面执行命令的返回内容
- **`send`** ：如果spawn后面运行命令的返回内容，匹配expect上面定义的。就发送send定义的内容到上面（相当于输入了密码）。

##### save\_images.sh

```ruby
cat > save_images.sh << eric
#!/bin/bash
# @Time    : 2019/11/26
# @Author  : Eric.Mao

# 定义Map
declare -A map=()
map["004"]="paas-login:1.0.0"
map["005"]="paas-system:1.0.0"
map["006"]="paas-importcheck:1.0.0"

# 镜像名称前缀
image_prefix=sinoeyes.io/dev2/

# 循环打印所有传入的参数
for i in "\$@"; do
    img=\${map["\$i"]}
    # 合法文件名
    new_path=\$i-\${img/:/-}'.tar'

    echo -e "\033[34m ######## 1 开始下载镜像 \033[0m   \033[35m $new_path \033[0m   \033[34m ######## \033[0m"
    # 下载本地镜像
    docker save -o \$new_path \$image_prefix\$img
    echo -e "\033[32m 镜像下载完成 \033[0m"

# shell 嵌入 expect 语法
expect << EOF
    # 设置超时时间
    set timeout 28800
    send_user "\n ======== 开始远程传输 \$new_path ======== \n"
    # 远程传输
    spawn scp -P 远程端口 \$new_path root@远程IP:/home/images
    expect {
        "yes/no" { send "yes\n"}
        "password:" { send "远程密码\n" }
    }
    expect eof
    send_user "\n ======== 远程传输完成 ======== \n"
EOF

done

eric

```
