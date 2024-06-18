---
title: 'webpack打包koa项目[转载]'
date: '2021-12-31T07:45:10+00:00'
status: publish
permalink: /2021/12/31/webpack%e6%89%93%e5%8c%85koa%e9%a1%b9%e7%9b%ae%e8%bd%ac%e8%bd%bd
author: 毛巳煜
excerpt: ''
type: post
id: 8222
category:
    - webpack
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
webpack打包koa项目配置解析

以前刚接触webpack的时候，我对它繁琐复杂的配置一个头两个大，后来项目渐渐做的多了，懂得多了，就渐渐熟悉了，而且也深深的理解了它的好处。

不管是做前端项目，还是用node做后端项目，只要和js相关的，都可以用webpack辅助构建，它可以提供es6语法的支持、开发热更新、部署代码压缩、对各种资源文件的处理……等等许多功能。

下面介绍在node框架koa开发的项目中，如何进行webpack配置。

一、新建koa项目
---------

新建`koa-demo`文件夹，通过npm初始化项目。然后创建以下目录结构、文件和内容：

**项目目录**

```diff
  koa-demo
  |- package.json
<span class="hljs-addition">+ |- /src</span>
<span class="hljs-addition">+ |- index.js</span>

```

**src/index.js**

```javascript
<span class="hljs-comment">// 先npm安装koa </span>
<span class="hljs-comment">// 这里引用和初始化</span>
<span class="hljs-keyword">const</span> Koa = <span class="hljs-built_in">require</span>(<span class="hljs-string">'koa'</span>)
<span class="hljs-keyword">const</span> app = <span class="hljs-keyword">new</span> Koa()

app.use(<span class="hljs-keyword">async</span> ctx => {
  ctx.body = <span class="hljs-string">'hello koa'</span>
})

<span class="hljs-comment">// 监听端口</span>
app.listen(<span class="hljs-number">3000</span>)

```

这样一个简单的koa项目就创建好了。

二、配置webpack
-----------

接下来就是重点了，配置webpack，我们先安装相关所有需要的依赖，再解释为什么要这样配置：

注：**这里所有配置以webpack4版本为基础**，升级webpack5可去官方查看

```bash
npm i -D webpack@4 webpack-cli@3
<span class="hljs-comment"># 安装webpack4版本</span>
<span class="hljs-comment"># 安装webpack-cli3版本 此工具用于在命令行中运行 webpack</span>

npm i -D clean-webpack-plugin
<span class="hljs-comment"># 常用插件，打包前自动清理之前打包的文件</span>

npm i -D webpack-node-externals
<span class="hljs-comment"># 打包时排除node_modules，里面的所有依赖都不打包</span>

npm i -D @babel/core @babel/node @babel/preset-env babel-loader
<span class="hljs-comment"># 使用es6语法所需的babel相关依赖</span>
<span class="hljs-comment"># @babel/node在babel7中被移了出来，如果在node环境中使用，要单独安装，有在运行Babel预设和插件之前进行编译的好处，调试用</span>

npm i -D terser-webpack-plugin@4
<span class="hljs-comment"># 生产环境需要打包压缩代码</span>

npm i -D webpack-merge
<span class="hljs-comment"># 分开发配置和生产配置，它们有共同配置，抽离出来，通过webpack-merge合并</span>

npm i -D nodemon
<span class="hljs-comment"># 监控node.js 源代码的变化和自动重启服务</span>

npm i -D cross-env
<span class="hljs-comment"># 运行跨平台设置和使用环境变量的脚本</span>

npm i -D npm-run-all
<span class="hljs-comment"># 实现同时执行多个命令</span>

npm i -D rimraf
<span class="hljs-comment"># 以包的形式包装rm -rf命令，用来删除文件和文件夹的。用来清理dist目录</span>

```

我们的koa项目分为**开发时环境**和**生产时环境**，不同环境时webpack的配置是有部分不同的，所以要新建两个配置文件`webpack.config.dev.js` 和 `webpack.config.prod.js`，同时它们又有共同之处，所以需要一个通用配置文件`webpack.config.base.js`。

所以在项目根目录下新建config文件夹，把这三个webpack配置文件放进去。

**项目目录**

```diff
  koa-demo
<span class="hljs-addition">+ |- config</span>
<span class="hljs-addition">+   |- webpack.config.base.js</span>
<span class="hljs-addition">+   |- webpack.config.dev.js</span>
<span class="hljs-addition">+   |- webpack.config.prod.js</span>
  |- package.json
  |- /src
    |- index.js

```

接下来在通用配置文件`webpack.config.base.js`中配置：

**config/webpack.config.base.js**

```javascript
<span class="hljs-keyword">const</span> path = <span class="hljs-built_in">require</span>(<span class="hljs-string">'path'</span>)
<span class="hljs-keyword">const</span> webpack = <span class="hljs-built_in">require</span>(<span class="hljs-string">'webpack'</span>)
<span class="hljs-keyword">const</span> nodeExternals = <span class="hljs-built_in">require</span>(<span class="hljs-string">'webpack-node-externals'</span>)
<span class="hljs-keyword">const</span> { CleanWebpackPlugin } = <span class="hljs-built_in">require</span>(<span class="hljs-string">'clean-webpack-plugin'</span>)

<span class="hljs-keyword">const</span> webpackConfig = {
  <span class="hljs-attr">target</span>: <span class="hljs-string">'node'</span>, <span class="hljs-comment">// koa项目仅在node环境下运行，因此设置称'node'</span>
  <span class="hljs-attr">entry</span>: {
    <span class="hljs-comment">// 设置入口文件</span>
    <span class="hljs-attr">server</span>: path.join(__dirname, <span class="hljs-string">'../src/index.js'</span>)
  },
  <span class="hljs-attr">output</span>: {
    <span class="hljs-comment">// 设置打包后的文件和位置</span>
    <span class="hljs-attr">filename</span>: <span class="hljs-string">'[name].bundle.js'</span>,
    <span class="hljs-attr">path</span>: path.join(__dirname, <span class="hljs-string">'../dist'</span>)
  },
  <span class="hljs-comment">// devtool: 'inline-source-map',</span>
  <span class="hljs-attr">module</span>: {
    <span class="hljs-attr">rules</span>: [
      {
        <span class="hljs-attr">test</span>: <span class="hljs-regexp">/\.js|jsx$/</span>,
        use: {
          <span class="hljs-attr">loader</span>: <span class="hljs-string">'babel-loader'</span>
        },
        <span class="hljs-comment">// 尽量将 loader 应用于最少数量的必要模块，因此设置include</span>
        <span class="hljs-comment">// 只针对该目录下的js文件进行babel处理</span>
        <span class="hljs-attr">include</span>: path.join(__dirname, <span class="hljs-string">'../src'</span>)
      }
    ]
  },
  <span class="hljs-attr">resolve</span>: {
    <span class="hljs-comment">// modules: 告诉webpack哪些目录需要搜索去匹配解析</span>
    <span class="hljs-attr">modules</span>: [path.join(__dirname, <span class="hljs-string">'../src/index.js'</span>), <span class="hljs-string">'node_modules'</span>],
    <span class="hljs-comment">// extensions: 告诉webpack这些后缀文件需要去搜索匹配</span>
    <span class="hljs-attr">extensions</span>: [<span class="hljs-string">'.js'</span>, <span class="hljs-string">'.json'</span>],
    <span class="hljs-attr">alias</span>: {
      <span class="hljs-comment">// 设置别名指向对应目录</span>
      <span class="hljs-string">'@'</span>: path.join(__dirname, <span class="hljs-string">'../src'</span>)
    }
  },
  <span class="hljs-attr">externals</span>: [nodeExternals()], <span class="hljs-comment">// 排除对node_modules里的依赖进行打包</span>
  <span class="hljs-attr">plugins</span>: [
    <span class="hljs-keyword">new</span> CleanWebpackPlugin(), <span class="hljs-comment">// 打包前清除输出目录</span>
    <span class="hljs-keyword">new</span> webpack.DefinePlugin({
      <span class="hljs-comment">// 定义环境变量，区分开发和生产环境</span>
      <span class="hljs-comment">// 具体详情可查看DefinePlugin文档</span>
      <span class="hljs-string">'process.env.NODE_ENV'</span>:
        process.env.NODE_ENV === <span class="hljs-string">'production'</span>
          ? <span class="hljs-built_in">JSON</span>.stringify(<span class="hljs-string">'production'</span>)
          : <span class="hljs-built_in">JSON</span>.stringify(<span class="hljs-string">'development'</span>)
    })
  ],
  <span class="hljs-comment">// node下这些选项可以使最初为Node.js环境编写的代码，在其他环境（如浏览器）中运行</span>
  <span class="hljs-attr">node</span>: {
    <span class="hljs-attr">console</span>: <span class="hljs-literal">true</span>,
    <span class="hljs-attr">global</span>: <span class="hljs-literal">true</span>,
    <span class="hljs-attr">process</span>: <span class="hljs-literal">true</span>,
    <span class="hljs-attr">Buffer</span>: <span class="hljs-literal">true</span>,
    <span class="hljs-attr">__filename</span>: <span class="hljs-literal">true</span>,
    <span class="hljs-attr">__dirname</span>: <span class="hljs-literal">true</span>,
    <span class="hljs-attr">setImmediate</span>: <span class="hljs-literal">true</span>,
    <span class="hljs-attr">path</span>: <span class="hljs-literal">true</span>
  }
}

<span class="hljs-built_in">module</span>.exports = webpackConfig

```

**config/webpack.config.dev.js**

```javascript
<span class="hljs-keyword">const</span> { merge } = <span class="hljs-built_in">require</span>(<span class="hljs-string">'webpack-merge'</span>)
<span class="hljs-keyword">const</span> baseConfig = <span class="hljs-built_in">require</span>(<span class="hljs-string">'./webpack.config.base'</span>)

<span class="hljs-comment">// 通过webpack-merge合并基础配置，添加开发时配置</span>
<span class="hljs-keyword">const</span> webpackConfig = merge(baseConfig, {
  <span class="hljs-attr">mode</span>: <span class="hljs-string">'development'</span>, <span class="hljs-comment">// 开发模式</span>
  <span class="hljs-attr">devtool</span>: <span class="hljs-string">'eval-source-map'</span>, <span class="hljs-comment">// 开发时出错能知道在源代码中哪一行</span>
  <span class="hljs-attr">stats</span>: {
    <span class="hljs-attr">children</span>: <span class="hljs-literal">false</span>, <span class="hljs-comment">// webpack打包时子模块信息设置不显示</span>
    <span class="hljs-attr">modules</span>: <span class="hljs-literal">false</span> <span class="hljs-comment">// 不显示模块信息</span>
  }
})

<span class="hljs-built_in">module</span>.exports = webpackConfig

```

**config/webpack.config.prod.js**

```javascript
<span class="hljs-keyword">const</span> { merge } = <span class="hljs-built_in">require</span>(<span class="hljs-string">'webpack-merge'</span>)
<span class="hljs-keyword">const</span> baseConfig = <span class="hljs-built_in">require</span>(<span class="hljs-string">'./webpack.config.base'</span>)
<span class="hljs-keyword">const</span> TerserPlugin = <span class="hljs-built_in">require</span>(<span class="hljs-string">'terser-webpack-plugin'</span>)

<span class="hljs-comment">// 通过webpack-merge合并基础配置，添加生产时配置</span>
<span class="hljs-keyword">const</span> webpackConfig = merge(baseConfig, {
  <span class="hljs-attr">mode</span>: <span class="hljs-string">'production'</span>, <span class="hljs-comment">// 生产模式</span>
  <span class="hljs-attr">stats</span>: {
    <span class="hljs-attr">children</span>: <span class="hljs-literal">false</span>, <span class="hljs-comment">// webpack打包时子模块信息设置不显示</span>
    <span class="hljs-attr">warnings</span>: <span class="hljs-literal">false</span> <span class="hljs-comment">// 警告不显示</span>
  },
  <span class="hljs-attr">optimization</span>: {
    <span class="hljs-attr">minimizer</span>: [
      <span class="hljs-comment">// terser-webpack-plugin插件可以压缩代码</span>
      <span class="hljs-comment">// 在webpack4版本中需要安装terser-webpack-plugin4版本</span>
      <span class="hljs-comment">// 里面是官方推荐的具体的参数，详情可查看文档</span>
      <span class="hljs-keyword">new</span> TerserPlugin({
        <span class="hljs-attr">terserOptions</span>: {
          <span class="hljs-attr">warning</span>: <span class="hljs-literal">true</span>,
          <span class="hljs-attr">compress</span>: {
            <span class="hljs-attr">warnings</span>: <span class="hljs-literal">false</span>,
            <span class="hljs-attr">drop_console</span>: <span class="hljs-literal">false</span>, <span class="hljs-comment">// 取消注释console 方便有时候进行调试</span>
            <span class="hljs-attr">dead_code</span>: <span class="hljs-literal">true</span>,
            <span class="hljs-attr">drop_debugger</span>: <span class="hljs-literal">true</span>
          },
          <span class="hljs-attr">output</span>: {
            <span class="hljs-attr">comments</span>: <span class="hljs-literal">false</span>, <span class="hljs-comment">// 不要注释</span>
            <span class="hljs-attr">beautify</span>: <span class="hljs-literal">false</span> <span class="hljs-comment">// 不要格式，一行显示所有代码</span>
          },
          <span class="hljs-attr">mangle</span>: <span class="hljs-literal">true</span>
        },
        <span class="hljs-attr">parallel</span>: <span class="hljs-literal">true</span>, <span class="hljs-comment">// 使用多进程并行运行可提高构建速度，默认的并发运行数量 os.cpus().length - 1</span>
        <span class="hljs-attr">sourceMap</span>: <span class="hljs-literal">false</span>
      })
    ],
    <span class="hljs-comment">// splitChunks 用来避免模块之间重复的依赖关系</span>
    <span class="hljs-attr">splitChunks</span>: {
      <span class="hljs-attr">cacheGroups</span>: {
        <span class="hljs-attr">commons</span>: {
          <span class="hljs-attr">name</span>: <span class="hljs-string">'commons'</span>,
          <span class="hljs-attr">chunks</span>: <span class="hljs-string">'initial'</span>,
          <span class="hljs-attr">minChunks</span>: <span class="hljs-number">3</span>,
          <span class="hljs-attr">enforce</span>: <span class="hljs-literal">true</span>
        }
      }
    }
  }
})

<span class="hljs-built_in">module</span>.exports = webpackConfig

```

### 1、配置babel去支持es6语法

接着在根目录下新建`.babelrc`文件，增加babel配置：

```json
{
  <span class="hljs-attr">"presets"</span>: [
    [
      <span class="hljs-string">"@babel/preset-env"</span>,
      {
        <span class="hljs-attr">"targets"</span>: {
          <span class="hljs-attr">"node"</span>: <span class="hljs-string">"current"</span>
        }
      }
    ]
  ]
}

```

改写src/index.js中的代码：

```diff
<span class="hljs-deletion">- const Koa = require('koa')</span>
<span class="hljs-addition">+ import Koa from 'koa'</span>
const app = new Koa()

app.use(async ctx => {
  ctx.body = 'hello koa'
})

// 监听端口
app.listen(3000)

```

如果我们用`node src/index.js`去运行，则会报错：

```shell
import Koa from 'koa'
^^^^^^

SyntaxError: Cannot use import statement outside a module

```

在在安装babel之后，node\_modules中提供了一个`babel-node`命令，我们可以通过该命令来运行我们的入口文件。

```bash
npx babel-node src/index.js

```

配合之前安装的`nodemon`可以实现热更新

```bash
npx nodemon --<span class="hljs-built_in">exec</span> babel-node src/index.js

```

我们在`package.json`中添加这个脚本：

```json
{
  <span class="hljs-attr">"script"</span>: {
    <span class="hljs-attr">"start"</span>: <span class="hljs-string">"nodemon --exec babel-node src/index.js"</span>
  }
}

```

这样通过在终端里运行`npm run start`即可启动项目了。

当然这个只是简单的实现去支持es6语法和开发时热更新功能，并没有通过用webpack去构建，在项目简单的情况下尚可。后面将介绍通过webpack去启动。

### 2、调试webpack配置文件

运行命令去监听webpack配置文件：

```bash
npx node --inspect-brk ./node_modules/.bin/webpack --config config/webpack.config.prod.js --progress
<span class="hljs-comment"># --config 指定要监听的配置文件</span>
<span class="hljs-comment"># --progress 打印webpack编译的过程</span>

```

可以在chrome浏览器里调试，也可以在编辑器里调试，具体方法见[node调试文档](https://link.juejin.cn?target=https%3A%2F%2Fnodejs.org%2Fen%2Fdocs%2Fguides%2Fdebugging-getting-started%2F "https://nodejs.org/en/docs/guides/debugging-getting-started/")。

![image-20210203165556606](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/3227b4e3ab0d4c919a06ae92860c4cd6~tplv-k3u1fbpfcp-watermark.awebp)

我们在`package.json`中添加这个脚本用来调试用：

```json
{
  <span class="hljs-attr">"script"</span>: {
    <span class="hljs-attr">"start"</span>: <span class="hljs-string">"nodemon --exec babel-node src/index.js"</span>,
    <span class="hljs-attr">"webpack:debug"</span>: <span class="hljs-string">"node --inspect-brk ./node_modules/.bin/webpack --config config/webpack.config.prod.js --progress"</span>
  }
}

```

### 3、通过webpack构建开发时环境

我们已经把开发时环境配置好了，接下来就是启动它，**通过`webpack --watch`命令来监听项目中文件的变化，如果其中一个文件被更新，代码将被重新编译**，而不必再去手动运行整个构建。

同时我们通过`cross-env`来设置环境变量，来指定当当前开发环境还是生产环境。

```bash
npx cross-env NODE_ENV=development webpack --watch --config config/webpack.config.dev.js --progress

```

执行该命令的意思就是，设置一个环境变量NODE\_ENV，值为development，因为我们之前在配置文件中通过DefinePlugin做了配置，所以当这个值不是production时就是开发环境，定义了对应的变量，在项目文件中就可以拿到这个变量，来针对开发和生产时做不同的逻辑处理。

设置了开发时的环境变量后，通过`webpack --watch`启动监听模式，指定开发时的配置文件`config/webpack.config.dev.js`文件，当项目中文件发生变化，代码将被重新编译打包输出到`dist/server.bundle.js`。

但仅仅这样时不够的，文件虽然重新被编译并打包了，但是我们并没有监听这个打包后的文件，因此我们通过`nodemon`来监听输出后的文件：

```bash
npx nodemon --inspect ./dist/server.bundle.js

```

我们这时候将不再简单的监听原始入口文件`src/index.js`了，而是监听经过了webpack处理（包括babel转换、代码压缩等）打包后生成的文件。

通过运行上面这两个命令就可以帮助我们实现构建开发时环境。我们把该命令配置到`package.json`脚本中：

```json
{
  <span class="hljs-attr">"script"</span>: {
    <span class="hljs-attr">"start"</span>: <span class="hljs-string">"nodemon --exec babel-node src/index.js"</span>,
    <span class="hljs-attr">"webpack:debug"</span>: <span class="hljs-string">"node --inspect-brk ./node_modules/.bin/webpack --config config/webpack.config.prod.js --progress"</span>,
    <span class="hljs-attr">"watch"</span>: <span class="hljs-string">"cross-env NODE_ENV=development webpack --watch --config config/webpack.config.dev.js --progress"</span>,
    <span class="hljs-attr">"debug"</span>: <span class="hljs-string">"nodemon --inspect dist/server.bundle.js"</span>
  }
}

```

但是这是两个命令，一个终端控制台只能监听一个命令，如果每次启动项目都开两个终端比较麻烦，所以我们安装一个工具`npm-run-all`，来实现一个脚本同时执行多个命令。继续在`package.json`中添加脚本：

```json
{
  <span class="hljs-attr">"script"</span>: {
    <span class="hljs-attr">"start"</span>: <span class="hljs-string">"nodemon --exec babel-node src/index.js"</span>,
    <span class="hljs-attr">"webpack:debug"</span>: <span class="hljs-string">"node --inspect-brk ./node_modules/.bin/webpack --config config/webpack.config.prod.js --progress"</span>,
    <span class="hljs-attr">"watch"</span>: <span class="hljs-string">"cross-env NODE_ENV=development webpack --watch --config config/webpack.config.dev.js --progress"</span>,
    <span class="hljs-attr">"debug"</span>: <span class="hljs-string">"nodemon --inspect dist/server.bundle.js"</span>,
    <span class="hljs-attr">"start:dist"</span>: <span class="hljs-string">"npm-run-all -p watch debug"</span>
  }
}

```

`npm-run-all -p watch debug`命令的含义是并行执行watch和debug两个脚本命令`-p`是并行执行的意思。

配置好后，我们直接在终端运行即可**启动开发时环境**了：

```bash
npm run start:dist

```

然后就可以安心写koa项目代码啦。

### 4、项目打包，运用到生产环境

项目写好之后，我们需要打包部署到线上生产环境，这时候再通过`npm run start:dist`命令就不合适了，因此我们来配置下构建生产环境的打包命令。

```bash
npx cross-env NODE_ENV=production webpack --config config/webpack.config.prod.js

```

和上面构建开发环境的命令很类似，不过此时我们设置环境变量NODE\_ENV值为production，并指定配置文件`config/webpack.config.prod.js`文件去打包构建。

我们把该命令配置到`package.json`中：

```json
{
  <span class="hljs-attr">"script"</span>: {
    <span class="hljs-attr">"start"</span>: <span class="hljs-string">"nodemon --exec babel-node src/index.js"</span>,
    <span class="hljs-attr">"webpack:debug"</span>: <span class="hljs-string">"node --inspect-brk ./node_modules/.bin/webpack --config config/webpack.config.prod.js --progress"</span>,
    <span class="hljs-attr">"watch"</span>: <span class="hljs-string">"cross-env NODE_ENV=development webpack --watch --config config/webpack.config.dev.js --progress"</span>,
    <span class="hljs-attr">"debug"</span>: <span class="hljs-string">"nodemon --inspect dist/server.bundle.js"</span>,
    <span class="hljs-attr">"start:dist"</span>: <span class="hljs-string">"npm-run-all -p watch debug"</span>,
    <span class="hljs-attr">"build"</span>: <span class="hljs-string">"cross-env NODE_ENV=production webpack --config config/webpack.config.prod.js"</span>
  }
}

```

运行该命令：

```bash
npm run build

```

即完成了生产环境下的项目打包构建。

将整个项目目录除了`node_modules`文件夹，推送到线上服务器，然后运行`npm install`安装依赖，接着用node命令执行文件`node dist/server.bundle.js`把项目启动起来，通过服务器地址和暴露的端口既可以访问koa项目接口啦。

> 注：清除dist目录配置  
> 使用`npm run build`文件项目时每次都会生成一个dist目录，有时需要把dist目录全部删掉，除了在命令行使用rm -rf /dist/命令删除外，还可以使用rimraf命令：  
> 安装：`npm install -D rimraf`  
> 使用：`npx rimraf dist`  
> 我们将其配置到`package.json`中：
> 
> ```diff
> {
>   "script": {
>     ...
>     "build": "cross-env NODE_ENV=production webpack --config config/webpack.config.prod.js",
> <span class="hljs-addition">+   "clean": "rimraf dist"</span>
>   }
> }
> 
> ```
> 
> 然后通过运行该命令即可清除dist目录：
> 
> ```bash
> npm run clean
> 
> ```

三、配置eslint + prettier风格
-----------------------

我习惯写项目必配eslint，操作如下：

### 1、安装eslint

```bash
<span class="hljs-comment"># 安装eslint</span>
npm i eslint -D

<span class="hljs-comment"># eslint初始化</span>
npx eslint --init

<span class="hljs-comment"># 进入自定义选择项</span>
<span class="hljs-comment"># 1. 你想要怎么使用eslint？ To check syntax and find problems</span>
<span class="hljs-comment"># 2. 哪一种模块是你的项目使用的？ JavaScript modules</span>
<span class="hljs-comment"># 3. 选择哪一个框架？ None of these</span>
<span class="hljs-comment"># 4. 你想要使用TypeScript吗？ N</span>
<span class="hljs-comment"># 5. 你要运行在哪个环境？ Browser, Node</span>
<span class="hljs-comment"># 6. 你想要配置文件格式是哪个？ JavaScript</span>

<span class="hljs-comment"># 全部选择完成后，会在本地生成.eslintrc.js文件</span>

```

### 2、安装prettier

```bash
<span class="hljs-comment"># 安装相关配置依赖</span>
npm install --save-dev eslint-config-prettier
npm install --save-dev eslint-plugin-prettier
npm install --save-dev --save-exact prettier

```

然后在`.eslintrc.js`文件中添加配置：

```javascript
<span class="hljs-built_in">module</span>.exports = {
  ...
  <span class="hljs-attr">plugins</span>: [<span class="hljs-string">'prettier'</span>],
  <span class="hljs-attr">extends</span>: [<span class="hljs-string">'eslint:recommended'</span>, <span class="hljs-string">'prettier'</span>, <span class="hljs-string">'prettier/prettier'</span>],
  <span class="hljs-attr">rules</span>: {
    <span class="hljs-string">'prettier/prettier'</span>: <span class="hljs-string">'error'</span>
  }
}

```

具体的prettier规则可以新建一个`.prettierrc`文件设置。

```json
{
  <span class="hljs-attr">"semi"</span>: <span class="hljs-literal">false</span>, <span class="hljs-comment">// 结尾是否加分号</span>
  <span class="hljs-attr">"singleQuote"</span>: <span class="hljs-literal">true</span>, <span class="hljs-comment">// 是否使用单引号</span>
  <span class="hljs-attr">"printWidth"</span>: <span class="hljs-number">80</span>, <span class="hljs-comment">// 一行代码最长显示80的length</span>
  <span class="hljs-attr">"endOfLine"</span>: <span class="hljs-string">"auto"</span>,
  <span class="hljs-attr">"trailingComma"</span>: <span class="hljs-string">"none"</span> <span class="hljs-comment">// 对象或者数组结尾一项是否逗号</span>
}

```

> 注：如果在`.eslintrc.js`文件里直接设置规则也行，但是这样在后面提交检查执行lint-staged的命令`prettier --write`时，就无法拿到这个规则，而使用prettier默认的规则。  
> 因此我们需要新建`.prettierrc`文件去让它们识别。

另外为了增加验证效率，排除那些不需要验证规则的文件，比如`mode_modules`，可以新建`.eslintignore`和`.prettierignore`文件。

> 注：webstorm编辑器默认JavaScript文件最后分号结尾，如果上述prettier规则结尾不要分号，则会有个编辑器默认的warning：unterminated statement颜色，虽然没啥错，但是看着不爽，可以在编辑器里设置去掉warning。  
> ![image-20210202163811226](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/319ac278e96a41efa2d9dd11ab81da73~tplv-k3u1fbpfcp-watermark.awebp)

四、提交git前代码检查
------------

为了增强代码线上质量，可以在git提交到仓库前使用`husky`和`lint-staged`进行检查。

它们的功能就是在git提交时触发钩子，其中最重要的一个钩子是`pre-commit`，在提交代码前可以让我们配置具体做什么，比如运行一下代码检查，如果不符合eslint规则的就中止这次git提交，让你去检查代码问题。

配置它们很简单，先安装这两个工具。

```bash
npm install husky lint-staged --save-dev

```

然后在`package.json`中增加配置：

```json
{
  <span class="hljs-attr">"husky"</span>: {
    <span class="hljs-attr">"hooks"</span>: {
      <span class="hljs-attr">"pre-commit"</span>: <span class="hljs-string">"lint-staged"</span>
    }
  },
  <span class="hljs-attr">"lint-staged"</span>: {
    <span class="hljs-comment">// 匹配所有js文件，按顺序执行任务</span>
    <span class="hljs-attr">"*.js"</span>: [
      <span class="hljs-string">"prettier --write"</span>,
      <span class="hljs-string">"eslint"</span>,
      <span class="hljs-string">"git add"</span>
    ]
  }
}

```

git的hooks可以在.git文件下的hooks目录里去查看它们，我们可以理解为执行git操作过程中的一系列生命周期，就像vue生命周期一样，在提交时触发一个`pre-commit`钩子，里面可以执行提交前要做的事情。比如可以执行检查代码：

```json
{
  <span class="hljs-attr">"husky"</span>: {
    <span class="hljs-attr">"hooks"</span>: {
      <span class="hljs-attr">"pre-commit"</span>: <span class="hljs-string">"prettier --write"</span>
    }
  }
}

```

这样它就在提交前执行了prettier修复命令。但是这样有一个问题，就是它会检查项目所有的代码，而不是仅仅你这次提交的，所以我们需要`lint-staged`来解决这个问题，而且`lint-staged`中可以分任务去执行多个命令。

```json
{
  <span class="hljs-attr">"husky"</span>: {
    <span class="hljs-attr">"hooks"</span>: {
      <span class="hljs-attr">"pre-commit"</span>: <span class="hljs-string">"lint-staged"</span>
    }
  },
  <span class="hljs-attr">"lint-staged"</span>: {
    <span class="hljs-comment">// 匹配提交的所有js文件，按顺序执行任务</span>
    <span class="hljs-attr">"*.js"</span>: [
      <span class="hljs-string">"prettier --write"</span>,
      <span class="hljs-string">"eslint"</span>,
      <span class="hljs-string">"git add"</span>
    ]，
    <span class="hljs-comment">// 匹配提交的所有vue文件，按顺序执行任务</span>
    <span class="hljs-string">"*.vue"</span>: [...]
  }
}

```

上述检查js文件的任务就是，先通过`prettier --write *.js`命令修复文件中不符合规则的代码，执行完后再执行`eslint *.js`命令检查不符合eslint规则的代码，没问题后执行`git add *.js`将修复的文件（如果有修复更改）重新添加到暂存区，然后再执行提交操作。

这其中有任何一个任务没通过，则本地提交中止，显示报错信息，提醒你规范代码。

![image-20210204103753077](https://p3-juejin.byteimg.com/tos-cn-i-k3u1fbpfcp/96430396ad84438eb71bb2e5c399f2fb~tplv-k3u1fbpfcp-watermark.awebp)

通过以上所有基础配置，开发koa项目之前的构建环境已经搭建完成，接下来只需要安心写项目代码即可。

后续可针对这些配置，再加上koa系列相关基础中间件，做成脚手架，以减少重复搭建项目基础环境的成本。