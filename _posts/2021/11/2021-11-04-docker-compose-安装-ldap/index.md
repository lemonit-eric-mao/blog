---
title: "docker-compose 安装 ldap"
date: "2021-11-04"
categories: 
  - "ldap"
---

##### **前置条件**

服务器IP地址: 172.16.15.205

* * *

###### **创建docker-compose文件**

```ruby
cat > docker-compose.yaml << ERIC

version: '3'
services:
  # 服务器端
  openldap:
    image: osixia/openldap:1.5.0
    container_name: openldap
    restart: always
    ports:
      # 389 是业务端口，客户端链接的时候使用这个端口
      - 389:389
      - 636:636
    environment:
      LDAP_ORGANISATION: "test-openldap"
      LDAP_DOMAIN: "test.com"
      LDAP_ADMIN_PASSWORD: "123456"
      LDAP_CONFIG_PASSWORD: "123456"
    volumes:
      - ./config/ldap:/var/lib/ldap
      - ./config/slapd.d:/etc/ldap/slapd.d

  # web管理页面
  phpldapadmin:
    container_name: phpldapadmin
    image: osixia/phpldapadmin:0.9.0
    ports:
      - 8080:80
    environment:
      - PHPLDAPADMIN_HTTPS="false"
      - PHPLDAPADMIN_LDAP_HOSTS=openldap
    depends_on:
      - openldap

ERIC

```

* * *

* * *

* * *

###### 测试访问

- Web管理界面: http://172.16.15.205:8080
- 用户名：`cn=admin,dc=test,dc=com`(没错用户名就是这一串，一开始我也懵)
- 密码：123456

* * *

* * *

* * *
