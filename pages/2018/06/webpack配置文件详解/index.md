---
title: "webpack配置文件详解"
date: "2018-06-11"
categories: 
  - "webpack"
---

### 项目结构

```ruby
mao-siyu@pc:/mnt/1TB/devProject/oa/manage-system-temple$ tree
.
├── dist
│   ├── 6209c185fec92002f10360653a7987fa.jpeg
│   ├── 9798f64007ae3426b2336e57dae4149c.ttf
│   ├── bundle.js
│   └── index.html
├── package.json
├── package-lock.json
├── src
│   ├── css
│   │   └── style.css
│   ├── font
│   │   └── Microsoft_YaHei_Mono.ttf
│   ├── image
│   │   └── icon.jpeg
│   └── index.js
├── webpack_config
│   ├── webpack.dev.config.js
│   └── webpack.prod.config.js
└── webpack.config.js

6 directories, 13 files
mao-siyu@pc:/mnt/1TB/devProject/oa/manage-system-temple$
```

### webpack.config.js 不一定全用上, 但要多了解

```javascript
const path = require('path');
// 设定 HtmlWebpackPlugin
const HtmlWebpackPlugin = require('html-webpack-plugin');
// 清理 /dist 文件夹
const CleanWebpackPlugin = require('clean-webpack-plugin');

module.exports = {
  /*
   * 我们将在 entry 添加 src/print.js 作为新的入口起点（print），
   * 然后修改 output，以便根据入口起点名称动态生成 bundle 名称
   */
  entry: {
    app: './src/index.js',
    print: './src/print.js'
  },
  /*
   * 使用 inline-source-map 选项(webpack中自带)，
   * 这有助于解释说明我们的目的（仅解释说明，不要用于生产环境）
   */
  devtool: 'inline-source-map',
  /*
   * webpack-dev-server 为你提供了一个简单的 web 服务器，并且能够实时重新加载(live reloading)。
   * npm install --save-dev webpack-dev-server
   * 这个配置告知 webpack-dev-server，在 localhost:8080 下建立服务，将 dist 目录下的文件，作为可访问文件。
   */
  devServer: {
    contentBase: './dist'
  },
  plugins: [
    /*
     * 清理 /dist 文件夹
     * npm install clean-webpack-plugin --save-dev
     * 它会删除旧的 /dist文件。
     */
    new CleanWebpackPlugin(['dist']),
    /*
     * 设定 HtmlWebpackPlugin
     * npm install --save-dev html-webpack-plugin
     * 它会用新生成的 index.html 文件，把我们的原来的替换，所有的 bundle 会自动添加到 html 中。
     */
    new HtmlWebpackPlugin({
      title: '后台管理系统模板'
    })
  ],
  output: {
    filename: '[name].bundle.js',
    path: path.resolve(__dirname, 'dist')
  },
  /*
   * webpack 根据正则表达式，来确定应该查找哪些文件，并将其提供给指定的 loader。
   */
  rules: [
    /*
     * 加载CSS
     * npm install --save-dev style-loader css-loader
     * 在这种情况下，以 .css 结尾的全部文件，都将被提供给 style-loader 和 css-loader。
     */
    {
      test: /\.css$/,
      use: [
        'style-loader',
        'css-loader'
      ]
    },
    /*
     * 加载图片
     * npm install --save-dev file-loader
     * 在这种情况下，以 .png|.svg|.jpeg|.gif 结尾的全部文件，都将被提供给 file-loader。
     */
    {
      test: /\.(png|svg|jpeg|gif)$/,
      use: [
        'file-loader',
        {
          /*
           * npm install image-webpack-loader --save-dev
           * 增强加载处理图片功能
           */
          loader: 'image-webpack-loader',
          options: {
            bypassOnDebug: true, // webpack@1.x
            disable: true, // webpack@2.x and newer
          }
        }
      ]
    },
    /*
     * 加载字体
     * 在这种情况下，以 .woff|.woff2|.eot|.ttf|.otf 结尾的全部文件，都将被提供给 file-loader。
     */
    {
      test: /\.(woff|woff2|eot|ttf|otf)$/,
      use: [
        'file-loader'
      ]
    },
    /*
     * 加载数据
     * npm install --save-dev csv-loader
     * 在这种情况下，以 .csv|.tsv 结尾的全部文件，都将被提供给 csv-loader。
     */
    {
      test: /\.(csv|tsv)$/,
      use: [
        'csv-loader'
      ]
    },
    /*
     * 加载数据
     * npm install --save-dev xml-loader
     * 在这种情况下，以 .xml 结尾的全部文件，都将被提供给 xml-loader。
     */
    {
      test: /\.xml$/,
      use: [
        'xml-loader'
      ]
    }
  ]
};
```
