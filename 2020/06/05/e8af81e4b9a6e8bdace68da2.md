---
title: 证书转换
date: '2020-06-05T03:21:03+00:00'
status: publish
permalink: /2020/06/05/%e8%af%81%e4%b9%a6%e8%bd%ac%e6%8d%a2
author: 毛巳煜
excerpt: ''
type: post
id: 5346
category:
    - Linux服务器
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### **`.pfx`** 文件

```ruby
[root@test ~]# ll
dev-share.pfx
[root@test ~]#

```

- - - - - -

##### 将 **`.pfx`** 格式的证书转换为 **`.pem`** 文件格式

```ruby
[root@test ~]# openssl pkcs12 -in dev-share.pfx -nodes -out dev-share.pem
Enter Import Password: # 输入密码
MAC verified OK
[root@test ~]#
[root@test ~]# ll
dev-share.pfx
dev-share.pem
[root@test ~]#

```

- - - - - -

- - - - - -

- - - - - -

###### 从 **`.pem`文件** 中导出私钥 `.key`

```ruby
[root@test ~]# openssl rsa -in dev-share.pem -out eric.key
Enter pass phrase for dev-share.pem:
writing RSA key
[root@test ~]#

```

- - - - - -

###### 从 **`.pem`文件** 中导出证书 `.crt`

```ruby
openssl x509 -in dev-share.pem -out eric.crt

```

- - - - - -

###### 从 **`.pfx`文件** 中导出证书 `.cer` 文件

```ruby
[root@test ~]# openssl pkcs12 -in dev-share.pfx -nodes -nokeys -out eric.cer
Enter Import Password:
MAC verified OK
[root@test ~]#

```

- - - - - -

- - - - - -

- - - - - -

##### **`其它`**

###### 从 **`.crt`文件** 中导出证书 `.pem`

```ruby
openssl x509 -in eric.crt -out dev-share.pem -outform PEM

```

- - - - - -

###### 从 **`.cer`文件** 中导出证书 `.pem`

```ruby
openssl x509 -inform der -in eric.cer -out dev-share.pem

```

- - - - - -

###### `.pem` 转 `.p12`

```ruby
openssl pkcs12 -export -in dev-share.pem -out eric.p12 -inkey dev-share-key.pem

```

- - - - - -

###### linux查看 pem内容

```ruby
openssl x509 -in dev-share.pem  -noout -text

```

- - - - - -

###### 导入`jdk` keystore

```ruby
keytool -importkeystore -deststorepass 123456 -destkeypass 123456 -destkeystore sh.keystore -srckeystore eric.p12 -srcstoretype PKCS12

```

- - - - - -

###### 使用jdk查看pem内容

```ruby
keytool -printcert -file consul-client-ca.pem

```

- - - - - -

- - - - - -

- - - - - -