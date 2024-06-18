---
title: 学习使用WebAssembly
date: '2022-01-29T00:44:29+00:00'
status: private
permalink: /2022/01/29/%e5%ad%a6%e4%b9%a0%e4%bd%bf%e7%94%a8webassembly
author: 毛巳煜
excerpt: ''
type: post
id: 8266
category:
    - WebAssembly
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
#### [什么是 WebAssembly？](https://developer.mozilla.org/zh-CN/docs/WebAssembly/Using_the_JavaScript_API "什么是 WebAssembly？")

在深入了解 WebAssembly 之前，我们先来看一下什么是 Assembly。

汇编（Assembly）是一种底层编程语言，与 CPU 架构的机器级指令有着非常紧密的联系。换句话说，它离机器可理解的代码（称为机器代码）只差一个转换过程。这种转换过程称为**汇编**。

顾名思义，**WebAssembly** 可以理解为 Web 的汇编。它是一种类似于汇编语言的底层语言，有着紧凑的二进制格式，使你能够以接近原生的速度运行 Web 应用程序。它还为 C、C++和 Rust  
等语言提供了编译目标，从而使客户端应用程序能够以接近原生的性能运行在 Web 上。

此外，WebAssembly 被设计为与 JavaScript 并存，而不是替代后者。使用 WebAssembly JavaScript API，你可以在两种语言之间来回交换代码，而不会出现任何问题。这样，你就可以获得同时具备  
WebAssembly 的功能和性能，以及 JavaScript 的多功能和适应性的应用程序。这打开了一个 Web 应用程序的全新世界，我们可以在 Web 上运行很多原本不准备用于 Web 的代码和功能。

- - - - - -

##### 如何获取 WebAssembly 代码

有几种方法可用：

- 从头开始编写 WebAssembly 代码——除非你非常了解它的基础知识，否则完全不建议这样做。
- 从 C 编译为 WebAssembly
- 从 C++编译为 WebAssembly
- 从 Rust 编译为 WebAssembly
- 使用 **AssemblyScript** 将 Typescript 的一个严格变体编译为 WebAssembly。对于不熟悉 C/C++或 Rust 的 Web 开发人员来说，这是一个不错的选项。

本项目使用 **AssemblyScript** 方法进行开发

- - - - - -

##### 本项目是如何创建、安装、部署的

```ruby
mkdir web-assembly-example && cd web-assembly-example

```

- - - - - -

###### 初始化项目

```ruby
npm init

```

- - - - - -

###### 安装依赖

```ruby
npm install --save @assemblyscript/loader
npm install --save-dev assemblyscript

```

安装后，编译器提供了一个方便的脚手架实用程序来快速设置一个新的 AssemblyScript 项目

```ruby
web-assembly-example> npx asinit .

```

- - - - - -

##### 编译

###### 编译源代码

```ruby
npm run asbuild

```

我们得到了构建的普通版本和优化版本。

对于每个构建版本，都有一个 **`.wasm` 二进制文件**，一个 **`.wasm.map` 源码映射**，以及二进制文件的 **`.wat` 文本表示形式**。

文本表示形式是为了供人阅读，但现在我们无需阅读或理解它，使用 `AssemblyScript` 的目的之一就是我们不需要使用原始 WebAssembly。

- - - - - -

##### 测试 (记住，先编译后执行)

```ruby
npm test

```

- - - - - -

##### 目录讲解

```
web-assembly-example
.
│
├─assembly                 # 我们使用javascript语法糖编写的代码，这些代码最终会编译成assembly源代码
│      index.ts
│      tsconfig.json       # 如果一个目录下存在一个tsconfig.json文件，那么它意味着这个目录是TypeScript项目的根目录。 tsconfig.json文件中指定了用来编译这个项目的根文件和编译选项。
│
├─build                    # 这里存放编译后的、真正的assembly源代码
│      .gitignore
│
├─tests                    # 测试, 模块
│       index.html         # 测试, 在浏览器中使用WebAssembly
│       index.js           # 测试, 在Node.js中使用WebAssembly
│
│  .gitignore
│  asconfig.json
│  index.js
│  package-lock.json
│  package.json
│  README.md
└─ text.txt

```

**[项目地址](https://gitee.com/eric-mao/web-assembly-example/tree/base "项目地址")**

- - - - - -

- - - - - -

- - - - - -