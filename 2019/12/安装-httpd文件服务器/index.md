---
title: "安装 httpd文件服务器"
date: "2019-12-11"
categories: 
  - "linux服务器"
---

#### **docker-compose 安装**

**`注意`**：**httpd:alpine**镜像中的程序，默认已经开启了文件列表模式，不需要在做任何更改

**[镜像地址](https://hub.docker.com/_/httpd?tab=tags "镜像地址")**

首先，从镜像中导出配置文件，以备修改

```ruby
docker run --rm httpd:alpine3.15  cat /usr/local/apache2/conf/httpd.conf > config/httpd.conf

```

**docker-compose.yaml**

```yaml
cat > docker-compose.yaml << ERIC
version: '3.6'
services:
  httpd:
    image: httpd:alpine3.15
    container_name: httpd
    restart: always
    ports:
      - 1080:80
    volumes:
      - ./config/httpd.conf:/usr/local/apache2/conf/httpd.conf
      # 程序发布目录
      - ./config/htdocs:/usr/local/apache2/htdocs/

ERIC

```

* * *

* * *

* * *

* * *

* * *

* * *

##### **CentOS 7.x** 二进制安装

##### 1 安装

```ruby
[root@aliyun ~]# wget http://qiniu.dev-share.top/httpd.zip && unzip httpd.zip

[root@aliyun ~]# rpm -ivh httpd/* --force --nodeps

```

##### 2 启动

```ruby
[root@aliyun ~]# systemctl start httpd.service && systemctl status httpd.service && systemctl enable httpd.service
```

##### 3 查看测试页

浏览器打开测试：http://ip 测试页上有提示： 1 将资源文件放到这个目录 `/var/www/html/` 2 需要修改配置文件来关闭测试页，开启文件列表页 `/etc/httpd/conf.d/welcome.conf`

##### 4 开启文件列表

```ruby
[root@aliyun ~]# vim /etc/httpd/conf.d/welcome.conf
#
# This configuration file enables the default "Welcome" page if there
# is no default index page present for the root URL.  To disable the
# Welcome page, comment out all the lines below.
#
# NOTE: if this file is removed, it will be restored on upgrades.
#
<LocationMatch "^/+$">
#    开启测试页
#    Options -Indexes
#    开启目录文件访问
    Options +Indexes
    ErrorDocument 403 /.noindex.html
</LocationMatch>

<Directory /usr/share/httpd/noindex>
    AllowOverride None
    Require all granted
</Directory>

Alias /.noindex.html /usr/share/httpd/noindex/index.html
Alias /noindex/css/bootstrap.min.css /usr/share/httpd/noindex/css/bootstrap.min.css
Alias /noindex/css/open-sans.css /usr/share/httpd/noindex/css/open-sans.css
Alias /images/apache_pb.gif /usr/share/httpd/noindex/images/apache_pb.gif
Alias /images/poweredby.png /usr/share/httpd/noindex/images/poweredby.png
[root@aliyun ~]#

# 需要重启服务
[root@aliyun ~]# systemctl restart httpd.service
```

* * *

* * *

* * *

###### 修改端口为1080

```ruby
vim /etc/httpd/conf/httpd.conf

......
#Listen 12.34.56.78:80
#Listen 80
Listen 1080
......

# 需要重启服务
[root@aliyun ~]# systemctl restart httpd.service
```

* * *

* * *

* * *

###### 防止中文乱码、与文件名称全显

```ruby
vim /etc/httpd/conf/httpd.conf

......
## <Directory "此项配置只对/var/www/html这个目录下的文件有效">
<Directory "/var/www/html">
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted

    # 加入如下配置
    # 编码格式,防止中文乱码
    IndexOptions Charset=UTF-8
    # 根据文件名自动调整列宽
    IndexOptions NameWidth=*
</Directory>

......

# 需要重启服务
[root@aliyun ~]# systemctl restart httpd.service
```

* * *

* * *

* * *
