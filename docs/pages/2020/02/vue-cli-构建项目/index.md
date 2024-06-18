---
title: "Vue-cli 构建项目"
date: "2020-02-14"
categories: 
  - "vue"
---

###### 1 **[安装 vue-cli](https://cli.vuejs.org/zh/guide/installation.html#%E5%AE%89%E8%A3%85 "安装 vue-cli")**

```ruby
npm install -g @vue/cli
# OR
yarn global add @vue/cli
```

* * *

###### 2 创建项目

```ruby
# 快速创建项目
vue create web-manage-system

-----------------------------------------------------------------

Vue CLI v3.8.2
┌───────────────────────────┐
│  Update available: 4.2.2  │
└───────────────────────────┘
? Please pick a preset:
  default (babel, eslint)
> Manually select features

-----------------------------------------------------------------

 (*) Babel
 ( ) TypeScript
 ( ) Progressive Web App (PWA) Support
 (*) Router
 ( ) Vuex
 (*) CSS Pre-processors
>( ) Linter / Formatter
 ( ) Unit Testing
 ( ) E2E Testing

-----------------------------------------------------------------

  Sass/SCSS (with dart-sass)
  Sass/SCSS (with node-sass)
> Less
  Stylus

-----------------------------------------------------------------

  In dedicated config files
> In package.json

-----------------------------------------------------------------

# 一路回车
```
