---
title: "win7系统MongoDB启动运行"
date: "2017-11-16"
categories: 
  - "mongodb"
---

#### 引言一 单纯的启动MongoDB

> "F:\\Program Files\\MongoDB\\Server\\3.2\\bin\\mongod.exe" --dbpath "F:\\Program Files\\MongoDB\\data" \*\*这样做一直会有一个服务器的运行的cmd窗口显示，里面不断的输出监听log\*\*

#### 引言二 带日志的启动

> "F:\\Program Files\\MongoDB\\Server\\3.2\\bin\\mongod.exe" --dbpath "F:\\Program Files\\MongoDB\\data" --logpath "F:\\Program Files\\MongoDB\\Logs\\MongoDB.log" \*\*这样做一直会有一个服务器的运行的cmd窗口显示，但log会写到log文件中\*\*

#### 引言三 将配置信息 添加到一个配置文件中 然后每次读取这个配置文件 (创建一个mongod.cfg文件存放如下信息)

> logpath = F:\\Program Files\\MongoDB\\Logs\\MongoDB.log dbpath = F:\\Program Files\\MongoDB\\data 启动方式 "F:\\Program Files\\MongoDB\\Server\\3.2\\bin\\mongod.exe" --config "F:\\Program Files\\MongoDB\\mongod.cfg" \*\*\*\*这样做一直会有一个服务器的运行的cmd窗口显示，但log会写到log文件中\*\*\*\*

#### 最终解决方式 自启动配置 将它 加入到服务 (务必要使用管理员权限运行 CMD)

> "F:\\Program Files\\MongoDB\\Server\\3.2\\bin\\mongod.exe" --config "F:\\Program Files\\MongoDB\\mongod.cfg" --install --serviceName MongoDB 这样就创建了一个名称为MongoDB的服务，接下来就是使用： net start MongoDB 来启动服务， net stop MongoDB 停止服务；

```null
    如果服务名称重复 可以使用如下命令来删除 sc delete MongoDB
```
