---
title: "安装 react-native"
date: "2017-11-16"
categories: 
  - "移动端"
---

### 安装 react-native-cli

```ruby
mao-siyu@pc:/mnt/1TB/devProject/react-proejct$ sudo yarn global add react-native-cli
```

```ruby
mao-siyu@pc:/mnt/1TB/devProject/react-proejct$ sudo yarn global add react-native-cli
yarn global v1.3.2
[1/4] Resolving packages...
[2/4] Fetching packages...
[3/4] Linking dependencies...
[4/4] Building fresh packages...
success Installed "react-native-cli@2.0.1" with binaries:
      - react-native
Done in 13.80s.
mao-siyu@pc:/mnt/1TB/devProject/react-proejct$
```

### 创建项目

```ruby
mao-siyu@pc:/mnt/1TB/devProject/react-proejct$ react-native init ReactNativeTemplate
mao-siyu@pc:/mnt/1TB/devProject/react-proejct$
```

### 启动项目

```ruby
mao-siyu@pc:/mnt/1TB/devProject/react-proejct$ cd ReactNativeTemplate
mao-siyu@pc:/mnt/1TB/devProject/react-proejct/ReactNativeTemplate$ npm start

> ReactNativeTemplate@0.0.1 start /mnt/1TB/devProject/react-proejct/ReactNativeTemplate
> node node_modules/react-native/local-cli/cli.js start

Scanning folders for symlinks in /mnt/1TB/devProject/react-proejct/ReactNativeTemplate/node_modules (4ms)
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  Running Metro Bundler on port 8081. │
│                                                                              │
│  Keep Metro running while developing on any JS projects. Feel free to        │
│  close this tab and run your own Metro instance if you prefer.               │
│                                                                              │
│  https://github.com/facebook/react-native                                    │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘

Looking for JS files in
   /mnt/1TB/devProject/react-proejct/ReactNativeTemplate 


Metro Bundler ready.

Loading dependency graph, done.

```
