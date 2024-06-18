---
title: "Nginx 下载安装 (一)"
date: "2017-11-16"
categories: 
  - "nginx"
---

##### **[nginx 官网地址](http://nginx.org/en/linux_packages.html#stable "nginx 官网地址")**

###### **[下载地址](http://nginx.org/en/linux_packages.html#RHEL-CentOS "下载地址")**

* * *

###### 安装

```ruby
# 安装 yum工具
yum -y install yum-utils

# 添加yum源
cat > /etc/yum.repos.d/nginx.repo << ERIC

[nginx-stable]
name=nginx stable repo
baseurl=http://nginx.org/packages/centos/\$releasever/\$basearch/
gpgcheck=1
enabled=1
gpgkey=https://nginx.org/keys/nginx_signing.key
module_hotfixes=true

ERIC

# 下载安装
yum -y install nginx
```

* * *
