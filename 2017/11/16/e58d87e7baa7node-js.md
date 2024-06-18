---
title: 升级Node.js
date: '2017-11-16T11:02:49+00:00'
status: publish
permalink: /2017/11/16/%e5%8d%87%e7%ba%a7node-js
author: 毛巳煜
excerpt: ''
type: post
id: 111
category:
    - node.js
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
介绍
--

**nvm（Node Version Manager）**是一个用于管理Node.js版本的工具，可以让您轻松地在同一台计算机上安装、切换和管理多个不同版本的Node.js。

下载
--

**[Windows系统下载](https://github.com/coreybutler/nvm-windows/tags)**  
**[Linux系统下载](https://github.com/nvm-sh/nvm/tags)**

设置代理
----

**终端输入：**  
**设置npm\_mirror:**

```shell
nvm npm_mirror https://npmmirror.com/mirrors/npm/

```

**设置node\_mirror:**

```shell
nvm node_mirror https://npmmirror.com/mirrors/node/

```

使用
--

```shell
- `nvm arch`
  - 显示 Node.js 是否运行在 32 位或 64 位模式下。

- `nvm list [available]`
  - 列出已安装的 Node.js 版本。
  - 在末尾输入 "available" 来查看可以安装的版本。该命令别名为 `nvm ls`。

- `nvm current`
  - 显示当前活动的 Node.js 版本。

- `nvm install <version> [arch]`
  - 安装特定版本的 Node.js，"latest" 表示最新当前版本，"lts" 表示最近的 LTS 版本。
  - 您可以选择是否安装 32 位或 64 位版本（默认为系统架构）。
  - 使用 `--insecure` 来绕过远程下载服务器的 SSL 验证。

- `nvm uninstall <version>`
  - 卸载指定的 Node.js 版本。

- `nvm use [version] [arch]`
  - 切换到使用指定的 Node.js 版本。
  - 您可以选择使用 "latest"、"lts" 或 "newest"，"newest" 是最新安装的版本。
  - 您可以选择指定 32 位或 64 位架构。
  - 使用 `nvm use <arch>` 将继续使用所选版本，但切换到 32 位或 64 位模式。

- `nvm proxy [url]`
  - 设置要用于下载的代理。
  - 将 [url] 留空以查看当前代理。
  - 将 [url] 设置为 "none" 以删除代理。

- `nvm node_mirror [url]`
  - 设置 Node.js 镜像。
  - 默认为 https://nodejs.org/dist/。
  - 将 [url] 留空以使用默认 URL。

- `nvm npm_mirror [url]`
  - 设置 npm 镜像。
  - 默认为 https://github.com/npm/cli/archive/。
  - 将 [url] 留空以使用默认 URL。

- `nvm root [path]`
  - 设置 nvm 应存储不同版本的 Node.js 的目录。
  - 如果未设置 `<path>`，则将显示当前根目录。

- `nvm [--]version`
  - 显示 Windows 上正在运行的 nvm 的当前版本。
  - 该命令别名为 `nvm v`。

- `nvm on`
  - 启用 Node.js 版本管理。

- `nvm off`
  - 禁用 Node.js 版本管理。
</path></arch></version></version>
```

- - - - - -

- - - - - -

- - - - - -

### 使用 n 模块

> n模块是专门用来管理nodejs的版本，通过它可以升级node的版本，但win系统下不太适用。

#### 安装：

```bash
npm install n -g

```

#### 查看n模块版本：

```bash
n -V

```

#### 使用 n 模块升级node版本：

```bash
n 14.17.0 ## 升级到指定版本

n latest ## 升级到最新版本

n lts ## 升级到长期支持版本

n stable ## 升级到最新的稳定版本

```