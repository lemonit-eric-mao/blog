---
title: "pm2 启动node.js服务器"
date: "2019-08-04"
categories: 
  - "node-js"
---

###### 下载安装

```ruby
[mao_siyu@shared-server ~]$ cnpm i pm2 -g
[mao_siyu@shared-server ~]$ pm2 -v

                        -------------

__/\\\\\\\\\\\\\____/\\\\____________/\\\\____/\\\\\\\\\_____
 _\/\\\/////////\\\_\/\\\\\\________/\\\\\\__/\\\///////\\\___
  _\/\\\_______\/\\\_\/\\\//\\\____/\\\//\\\_\///______\//\\\__
   _\/\\\\\\\\\\\\\/__\/\\\\///\\\/\\\/_\/\\\___________/\\\/___
    _\/\\\/////////____\/\\\__\///\\\/___\/\\\________/\\\//_____
     _\/\\\_____________\/\\\____\///_____\/\\\_____/\\\//________
      _\/\\\_____________\/\\\_____________\/\\\___/\\\/___________
       _\/\\\_____________\/\\\_____________\/\\\__/\\\\\\\\\\\\\\\_
        _\///______________\///______________\///__\///////////////__


                          Runtime Edition

        PM2 is a Production Process Manager for Node.js applications
                     with a built-in Load Balancer.

                Start and Daemonize any application:
                $ pm2 start app.js

                Load Balance 4 instances of api.js:
                $ pm2 start api.js -i 4

                Monitor in production:
                $ pm2 monitor

                Make pm2 auto-boot at server restart:
                $ pm2 startup

                To go further checkout:
                http://pm2.io/


                        -------------

[PM2] Spawning PM2 daemon with pm2_home=/root/.pm2
[PM2] PM2 Successfully daemonized
4.2.3
[mao_siyu@shared-server ~]$
```

* * *

###### 启动

```ruby
[mao_siyu@shared-server travel-companion-server]$ pwd
/mnt/www/travel-companion-server
[mao_siyu@shared-server travel-companion-server]$
[mao_siyu@shared-server travel-companion-server]$ pm2 -n 约伴 start npm -- start
[PM2] Applying action restartProcessId on app [npm](ids: 0)
[PM2] [约伴](0) ✓
[PM2] Process successfully started
┌──────────┬────┬──────┬───────┬────────┬─────────┬────────┬─────┬──────────┬──────────┬──────────┐
│ App name │ id │ mode │ pid   │ status │ restart │ uptime │ cpu │ mem      │ user     │ watching │
├──────────┼────┼──────┼───────┼────────┼─────────┼────────┼─────┼──────────┼──────────┼──────────┤
│ 约伴      │ 0  │ fork │ 29101 │ online │ 1       │ 0s     │ 0%  │ 6.4 MB   │ mao_siyu │ disabled │
└──────────┴────┴──────┴───────┴────────┴─────────┴────────┴─────┴──────────┴──────────┴──────────┘
 Use `pm2 show <id|name>` to get more details about an app
[mao_siyu@shared-server travel-companion-server]$
```

* * *

* * *

* * *

##### 常见问题

```ruby

```
