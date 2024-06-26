---
title: "Nginx 证书部署"
date: "2017-12-11"
categories: 
  - "nginx"
---

##### 配置证书很简单, 先去腾讯申请的免费的证书, 按照提示进行操作即可!

```ruby
[root@zhujiwu conf.d]# cat word-press.conf

# 强制80端口跳转到443端口
server {
    listen                       80;
    server_name                  www.private-blog.com;
    return                       301 https://$server_name$request_uri;                     # 官方写法
    # rewrite                    ^(.*)$  https://$server_name$1 permanent;                  # 其它网站上的写法
}

# 配置证书
server {
    listen                       443 ssl;
    server_name                  www.private-blog.com;                                     # 填写绑定证书的域名
    ssl                          on;
    ssl_certificate              conf.d/1_www.private-blog.com_bundle.crt;                 # 默认路径是 /etc/nginx
    ssl_certificate_key          /etc/nginx/conf.d/2_www.private-blog.com.key;             # 也可以写绝对路径
    ssl_session_timeout          5m;
    ssl_protocols                TLSv1 TLSv1.1 TLSv1.2;                                    # 按照这个协议配置
    ssl_ciphers                  ECDHE-RSA-AES128-GCM-SHA256:HIGH:!aNULL:!MD5:!RC4:!DHE;  # 按照这个套件配置
    ssl_prefer_server_ciphers    on;

    location / {

        proxy_set_header         X-Real-IP $remote_addr;
        proxy_set_header         X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header         Host $http_host;
        proxy_set_header         X-NginX-Proxy true;

        proxy_pass               http://127.0.0.1:1888;
        proxy_redirect           off;

        # Socket.IO Support
        proxy_http_version       1.1;
        proxy_set_header         Upgrade $http_upgrade;
        proxy_set_header         Connection "upgrade";
    }

}

[root@zhujiwu conf.d]#
```

* * *

* * *

* * *

###### SSL 动态更新证书

```ruby
# 配置证书
server {
    listen                       443 ssl;

    # 例如请求的域名是 curl www.baidu.com 那么 $ssl_server_name.crt 就会变成 www.baidu.com.crt
    # 优点： 可以动态更新证书，无需reload，多域名使用同一个IP的情况下，不需要在额外配置
    # 缺点： 在初次使用时，动态读取证书，可能会造成20%~30%时间消耗， 但后续流量加密不受影响
    ssl_certificate              /etc/nginx/ssl/$ssl_server_name.crt;
    ssl_certificate_key          /etc/nginx/ssl/$ssl_server_name.key;
    ssl_protocols                TLSv1.3 TLSv1.2 TLSv1.1;
    ssl_prefer_server_ciphers    on;

    location / {

        proxy_set_header         Host $host;
        proxy_pass               http://127.0.0.1:1888;
    }

}
```

* * *

* * *

* * *
