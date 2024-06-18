---
title: Vue.js学习（一）
date: '2017-11-16T12:54:00+00:00'
status: publish
permalink: /2017/11/16/vue-js%e5%ad%a6%e4%b9%a0%ef%bc%88%e4%b8%80%ef%bc%89
author: 毛巳煜
excerpt: ''
type: post
id: 226
category:
    - vue
tag: []
post_format: []
hestia_layout_select:
    - default
---
Vue.js学习（一）
-----------

#### 安装Vue.js

```
<pre data-language="">```
Vue.js 提供一个官方命令行工具，可用于快速搭建大型单页应用。
该工具提供开箱即用的构建工具配置，带来现代化的前端开发流程。
只需几分钟即可创建并启动一个带热重载、保存时静态检查以及可用于生产环境的构建配置的项目：

```
```

```
<pre data-language="">```ruby
// 全局安装 vue-cli
<span class="katex math inline">npm install -g vue-cli</span> vue -V
2.8.1

// 创建一个基于 webpack 模板的新项目
<span class="katex math inline">vue init webpack my-project

// 安装依赖</span> cd my-project
<span class="katex math inline">npm install</span> npm run dev

```
```

#### 直接应用 Vue.js

##### index.html 双向绑定示例

```
<pre data-language="HTML">```markup



    <meta charset="UTF-8"></meta>
    <title>Vue.js demo</title>
    <script src="../public/javascript/vue.js"></script>


<div id="scope">
    <p>{{info}}</p>
    <p>{{messsage}}</p>
    <input type="text" v-model="info"></input>
</div>

<script>
    new Vue({
        // &#36890;&#36807;&#20803;&#32032;&#30340;id&#26469;&#35774;&#23450;&#25968;&#25454;&#30340;&#21487;&#25805;&#20316;&#33539;&#22260;
        el: '#scope',
        // &#25552;&#20379;&#25968;&#25454;
        data: {
            info: 'Hello world! vue.js',
            messsage: '666666'
        }
    });
</script>


```
```

#### 绑定Dom属性

```
<pre data-language="HTML">```markup
v-bind 缩写


<a v-bind:href="url"></a>

<a :href="url"></a>





    <meta charset="UTF-8"></meta>
    <title>Vue.js demo</title>
    <script src="../public/javascript/vue.js"></script>


<div id="scope">
    <p :class="clazz">{{info}}</p>
    <input :value="clazz" type="text"></input>
    <br></br>
    <input type="text" v-model="info"></input>
</div>

<script>
    new Vue({
        // &#36890;&#36807;&#20803;&#32032;&#30340;id&#26469;&#35774;&#23450;&#25968;&#25454;&#30340;&#21487;&#25805;&#20316;&#33539;&#22260;
        el: '#scope',
        // &#25552;&#20379;&#25968;&#25454;
        data: {
            info: 'Hello world! vue.js',
            messsage: '666666',
            clazz: 'red'
        },
        method: {}
    });
</script>



```
```

#### 绑定元素事件

```
<pre data-language="HTML">```markup
v-on 缩写


<a v-on:click="doSomething"></a>

<a></a>





    <meta charset="UTF-8"></meta>
    <title>Vue.js demo</title>
    <script src="../public/javascript/vue.js"></script>


<div id="scope">
    <p>{{info}}</p>
    <input type="button" value="弹出alert"></input>
</div>

<script>
    new Vue({
        // &#36890;&#36807;&#20803;&#32032;&#30340;id&#26469;&#35774;&#23450;&#25968;&#25454;&#30340;&#21487;&#25805;&#20316;&#33539;&#22260;
        el: '#scope',
        // &#25552;&#20379;&#25968;&#25454;
        data: {
            info: 'Hello world! vue.js',
            messsage: '666666',
            clazz: 'red'
        },
        methods: {
            showAlert: function () {
                alert('&#20320;&#28857;&#21040;&#25105;&#21862;&#65281;&#25343;&#38065;~~~');
            }
        }
    });
</script>


```
```