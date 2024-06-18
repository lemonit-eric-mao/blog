---
title: "React 学习-安装"
date: "2018-03-29"
categories: 
  - "前端开发"
---

### 开发环境

```ruby
mao-siyu@mao-siyu-PC:~/文档/code/react-demo$ node -v
v8.10.0
mao-siyu@mao-siyu-PC:~/文档/code/react-demo$ npm -v
5.6.0
mao-siyu@mao-siyu-PC:~/文档/code/react-demo$ yarn -v
1.5.1
```

# create-react-app 脚手架 适用于学习

#### 创建项目

```ruby
mao-siyu@mao-siyu-PC:~/文档/code/react-demo$ npx create-react-app my-app
mao-siyu@mao-siyu-PC:~/文档/code/react-demo$ ll
总用量 12
drwxrwxr-x  3 mao-siyu mao-siyu 4096 3月  29 15:26 ./
drwxrwxr-x 30 mao-siyu mao-siyu 4096 3月  29 11:32 ../
drwxrwxr-x  5 mao-siyu mao-siyu 4096 3月  29 15:26 my-app/
mao-siyu@mao-siyu-PC:~/文档/code/react-demo$ cd my-app/
```

#### 启动项目Demo

```ruby
mao-siyu@mao-siyu-PC:~/文档/code/react-demo/my-app$ npm start
Compiled successfully!

You can now view my-app in the browser.

  Local:            http://localhost:3000/
  On Your Network:  http://10.32.158.154:3000/

Note that the development build is not optimized.
To create a production build, use yarn build.
```

# rekit 脚手架 适用于大型项目

```ruby
# 安装 rekit
mao-siyu@pc:/mnt/1TB/devProject/react-proejct$ sudo npm install -g rekit
# 使用 rekit 创建 react 项目
mao-siyu@pc:/mnt/1TB/devProject/react-proejct$ rekit create MyReactDemo
mao-siyu@pc:/mnt/1TB/devProject/react-proejct$ cd MyReactDemo/
mao-siyu@pc:/mnt/1TB/devProject/react-proejct/MyReactDemo$ npm i
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
