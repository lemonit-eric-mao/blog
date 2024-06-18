---
title: "npm 常用命令"
date: "2020-02-14"
categories: 
  - "node-js"
---

###### 前置条件

```json
{
  "name": "travel-companion-server",
  "version": "0.0.0",
  "private": true,
  "scripts": {
    "start": "node ./bin/www",
    "dev": "node ./bin/www"
  },
  "author": "eric.mao",
  "license": "ISC",
  "devDependencies": {},
  "dependencies": {
  }
}

```

* * *

###### 启动项目

```ruby
# start 命令启动
[root@dev2 project]# npm start
# 其它命令 启动必须要加 run
[root@dev2 project]# npm run dev
```

* * *

###### 指定项目运行(package.json所在目录)

```ruby
[root@dev2 project]# npm --prefix /home/project/web-manage i
# 或
[root@dev2 project]# cnpm --prefix /home/project/web-manage i
```

* * *

###### `npm --prefix=` 解释

```ruby
###### 在awx/ui_next目录下执行    npm install
npm --prefix=awx/ui_next install

###### 在awx/ui_next目录下执行    npm start
npm --prefix=awx/ui_next start
```

* * *

###### npm 创建项目

```ruby
mkdir html2image

cd html2image

npm init
```

* * *
