---
title: '安装 react-native'
date: '2017-11-16T16:47:18+00:00'
status: publish
permalink: /2017/11/16/%e5%ae%89%e8%a3%85-react-native
author: 毛巳煜
excerpt: ''
type: post
id: 571
category:
    - 移动端
tag: []
post_format: []
hestia_layout_select:
    - default
---
### 安装 react-native-cli

```
<pre data-language="">```ruby
mao-siyu@pc:/mnt/1TB/devProject/react-proejct$ sudo yarn global add react-native-cli

```
```

```
<pre data-language="">```ruby
mao-siyu@pc:/mnt/1TB/devProject/react-proejct<span class="katex math inline">sudo yarn global add react-native-cli
yarn global v1.3.2
[1/4] Resolving packages...
[2/4] Fetching packages...
[3/4] Linking dependencies...
[4/4] Building fresh packages...
success Installed "react-native-cli@2.0.1" with binaries:
      - react-native
Done in 13.80s.
mao-siyu@pc:/mnt/1TB/devProject/react-proejct</span>

```
```

### 创建项目

```
<pre data-language="">```ruby
mao-siyu@pc:/mnt/1TB/devProject/react-proejct<span class="katex math inline">react-native init ReactNativeTemplate
mao-siyu@pc:/mnt/1TB/devProject/react-proejct</span>

```
```

### 启动项目

```
<pre data-language="">```ruby
mao-siyu@pc:/mnt/1TB/devProject/react-proejct<span class="katex math inline">cd ReactNativeTemplate
mao-siyu@pc:/mnt/1TB/devProject/react-proejct/ReactNativeTemplate</span> npm start

> ReactNativeTemplate@0.0.1 start /mnt/1TB/devProject/react-proejct/ReactNativeTemplate
> node node_modules/react-native/local-cli/cli.js start

Scanning folders for symlinks in /mnt/1TB/devProject/react-proejct/ReactNativeTemplate/node_modules (4ms)
┌──────────────────────────────────────────────────────────────────────────────┐
│                                                                              │
│  Running Metro Bundler on port 8081.                                         │
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
```