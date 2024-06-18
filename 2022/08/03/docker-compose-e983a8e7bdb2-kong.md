---
title: 'docker-compose 部署 Kong'
date: '2022-08-03T08:30:56+00:00'
status: publish
permalink: /2022/08/03/docker-compose-%e9%83%a8%e7%bd%b2-kong
author: 毛巳煜
excerpt: ''
type: post
id: 9030
category:
    - Kong
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### **[Kong lua 插件开发](http://www.dev-share.top/2022/08/08/kong-lua-%e6%8f%92%e4%bb%b6%e5%bc%80%e5%8f%91/ "Kong lua 插件开发")**

- - - - - -

#### 部署 Kong 网关 测试插件

###### 使用docker-compose部署 kong 网关

```ruby
cat > docker-compose.yaml 
```

- - - - - -

##### 把自定义插件加入服务中

1. **先把代码(`handler.lua`、`schema.lua`)放到 `./config/plugins/lua-encrypt`文件夹下，`/lua-encrypt` Kong会将文件夹的名做为插件的名**
2. **修改`/etc/kong/kong.conf`文件，告诉 Kong 服务启动的时候要加载自定义插件**

```ruby
cat >> config/kong/kong.conf 
```

**kong.conf配置文件解释说明**

```ruby
## 指定自定义插件目录
## 我们的插件准备放在容器中的/opt/share/kong/plugins目录下(这个目录是由docker-compose启动容器时自动创建的)
## 注意指定插件目录前缀(不能包含/kong/plugins)
lua_package_path = /opt/share/?.lua;;

## 一般情况下/etc/kong里是没有kong.conf，只有kong.conf.default和kong.logrotate
## 把kong.conf.default拷贝成kong.conf即可生效(这里采用了docker-compose替换文件的方式来做)
#### 解释: plugins = bundled,<plugin-name>
#### 如果你不需要kong自带的插件，可以取消掉 bundled (bundled 就是指/usr/local/share/lua/5.1/kong/plugins目录中的默认插件是否使用)
#### lua-encrypt是自定义插件的名称
plugins = bundled,lua-encrypt

</plugin-name>
```

- - - - - -

- - - - - -

- - - - - -

###### 启动 Kong 服务

```ruby
docker-compose up -d


## 查看结果
[root@centos01 ~]# docker-compose ps
     Name                   Command                  State                                                                   Ports
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
kong-database    docker-entrypoint.sh postgres    Up (healthy)   0.0.0.0:5432->5432/tcp,:::5432->5432/tcp
kong-gateway     /docker-entrypoint.sh kong ...   Up (healthy)   0.0.0.0:8000->8000/tcp,:::8000->8000/tcp, 0.0.0.0:8001->8001/tcp,:::8001->8001/tcp, 0.0.0.0:8443->8443/tcp,:::8443->8443/tcp,
                                                                 8444/tcp
kong-gui         /app/start.sh                    Up             0.0.0.0:1337->1337/tcp,:::1337->1337/tcp
kong-migration   /docker-entrypoint.sh kong ...   Exit 0
konga-prepare    /app/start.sh -c prepare - ...   Exit 0


```

- - - - - -

###### 测试

访问Web: http://127.0.0.1:1337

- - - - - -

- - - - - -

- - - - - -