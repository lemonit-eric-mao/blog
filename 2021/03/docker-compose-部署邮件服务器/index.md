---
title: "docker-compose 部署邮件服务器"
date: "2021-03-17"
categories: 
  - "运维"
---

###### 前置条件

本机IP： 124.93.26.39

* * *

###### docker-compose文件

```ruby
cat > docker-compose.yaml << ERIC
version: '3'
services:
  mail:
    image: bestwu/ewomailserver
    container_name: ewomail
    restart: always
    hostname: mail.dev-share.com
    extra_hosts:
      - mail.dev-share.com:124.93.26.39
    ports:
      - 25:25
      - 143:143
      - 587:587
      - 993:993
      - 109:109
      - 110:110
      - 465:465
      - 995:995
      - 1080:80
      - 8081:8080
    volumes:
      - /etc/localtime:/etc/localtime:ro
      - ./config/mysql:/ewomail/mysql/data
      - ./config/vmail:/ewomail/mail
      - ./config/rainloop:/ewomail/www/rainloop/data
      - ./config/ssl/certs/:/etc/ssl/certs/
      - ./config/ssl/private/:/etc/ssl/private/
      - ./config/ssl/dkim/:/ewomail/dkim/
ERIC

```

* * *

- 邮箱管理后台: http://124.93.26.39:8081
- 默认用户: admin
- 默认密码: ewomail123

* * *

- Rainloop 管理端: http://124.93.26.39:1080/?admin
- 默认用户: admin
- 默认密码: 12345

* * *

- Rainloop 用户端: http://124.93.26.39:1080

* * *
