---
title: "Vue.js学习（一）"
date: "2017-11-16"
categories: 
  - "vue"
---

## Vue.js学习（一）

#### 安装Vue.js

```
Vue.js 提供一个官方命令行工具，可用于快速搭建大型单页应用。
该工具提供开箱即用的构建工具配置，带来现代化的前端开发流程。
只需几分钟即可创建并启动一个带热重载、保存时静态检查以及可用于生产环境的构建配置的项目：
```

```ruby
// 全局安装 vue-cli
$ npm install -g vue-cli
$ vue -V
2.8.1

// 创建一个基于 webpack 模板的新项目
$ vue init webpack my-project

// 安装依赖
$ cd my-project
$ npm install
$ npm run dev
```

#### 直接应用 Vue.js

##### index.html 双向绑定示例

```markup
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Vue.js demo</title>
    <script src="../public/javascript/vue.js"></script>
</head>
<body>
<div id="scope">
    <p>{{info}}</p>
    <p>{{messsage}}</p>
    <input type="text" v-model="info"/>
</div>
</body>
<script>
    new Vue({
        // 通过元素的id来设定数据的可操作范围
        el: '#scope',
        // 提供数据
        data: {
            info: 'Hello world! vue.js',
            messsage: '666666'
        }
    });
</script>
</html>
```

#### 绑定Dom属性

```markup
v-bind 缩写

<!-- 完整语法 -->
<a v-bind:href="url"></a>
<!-- 缩写 -->
<a :href="url"></a>

<!-- 完整示例 -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Vue.js demo</title>
    <script src="../public/javascript/vue.js"></script>
</head>
<body>
<div id="scope">
    <p :class="clazz">{{info}}</p>
    <input type="text" :value="clazz"/>
    <br>
    <input type="text" v-model="info"/>
</div>
</body>
<script>
    new Vue({
        // 通过元素的id来设定数据的可操作范围
        el: '#scope',
        // 提供数据
        data: {
            info: 'Hello world! vue.js',
            messsage: '666666',
            clazz: 'red'
        },
        method: {}
    });
</script>
</html>

```

#### 绑定元素事件

```markup
v-on 缩写

<!-- 完整语法 -->
<a v-on:click="doSomething"></a>
<!-- 缩写 -->
<a @click="doSomething"></a>

<!-- 完整示例 -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Vue.js demo</title>
    <script src="../public/javascript/vue.js"></script>
</head>
<body>
<div id="scope">
    <p>{{info}}</p>
    <input type="button" @click="showAlert" value="弹出alert"/>
</div>
</body>
<script>
    new Vue({
        // 通过元素的id来设定数据的可操作范围
        el: '#scope',
        // 提供数据
        data: {
            info: 'Hello world! vue.js',
            messsage: '666666',
            clazz: 'red'
        },
        methods: {
            showAlert: function () {
                alert('你点到我啦！拿钱~~~');
            }
        }
    });
</script>
</html>
```
