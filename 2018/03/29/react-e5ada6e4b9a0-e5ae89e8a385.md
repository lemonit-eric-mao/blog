---
title: 'React 学习-安装'
date: '2018-03-29T15:32:26+00:00'
status: publish
permalink: /2018/03/29/react-%e5%ad%a6%e4%b9%a0-%e5%ae%89%e8%a3%85
author: 毛巳煜
excerpt: ''
type: post
id: 2049
category:
    - 前端开发
tag: []
post_format: []
---
### 开发环境

```
<pre data-language="">```ruby
mao-siyu@mao-siyu-PC:~/文档/code/react-demo<span class="katex math inline">node -v
v8.10.0
mao-siyu@mao-siyu-PC:~/文档/code/react-demo</span> npm -v
5.6.0
mao-siyu@mao-siyu-PC:~/文档/code/react-demo$ yarn -v
1.5.1

```
```

create-react-app 脚手架 适用于学习
==========================

#### 创建项目

```
<pre data-language="">```ruby
mao-siyu@mao-siyu-PC:~/文档/code/react-demo<span class="katex math inline">npx create-react-app my-app
mao-siyu@mao-siyu-PC:~/文档/code/react-demo</span> ll
总用量 12
drwxrwxr-x  3 mao-siyu mao-siyu 4096 3月  29 15:26 ./
drwxrwxr-x 30 mao-siyu mao-siyu 4096 3月  29 11:32 ../
drwxrwxr-x  5 mao-siyu mao-siyu 4096 3月  29 15:26 my-app/
mao-siyu@mao-siyu-PC:~/文档/code/react-demo$ cd my-app/

```
```

#### 启动项目Demo

```
<pre data-language="">```ruby
mao-siyu@mao-siyu-PC:~/文档/code/react-demo/my-app$ npm start
Compiled successfully!

You can now view my-app in the browser.

  Local:            http://localhost:3000/
  On Your Network:  http://10.32.158.154:3000/

Note that the development build is not optimized.
To create a production build, use yarn build.

```
```

rekit 脚手架 适用于大型项目
=================

```
<pre data-language="">```ruby
# 安装 rekit
mao-siyu@pc:/mnt/1TB/devProject/react-proejct<span class="katex math inline">sudo npm install -g rekit
# 使用 rekit 创建 react 项目
mao-siyu@pc:/mnt/1TB/devProject/react-proejct</span> rekit create MyReactDemo
mao-siyu@pc:/mnt/1TB/devProject/react-proejct<span class="katex math inline">cd MyReactDemo/
mao-siyu@pc:/mnt/1TB/devProject/react-proejct/MyReactDemo</span> npm i
# 启动项目
mao-siyu@pc:/mnt/1TB/devProject/react-proejct/MyReactDemo$ npm start
Compiled successfully!

You can now view MyReactDemo in the browser.

  Local:            http://localhost:6075/
  On Your Network:  http://192.168.1.16:6075/

Note that the development build is not optimized.
To create a production build, use npm run build.

To use Rekit Studio, access: http://localhost:6076

```
```