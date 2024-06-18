---
title: 'Nuxt.js $router 与 $route'
date: '2017-12-12T23:33:29+00:00'
status: publish
permalink: /2017/12/12/nuxt-js-router-%e4%b8%8e-route
author: 毛巳煜
excerpt: ''
type: post
id: 1743
category:
    - vue
tag: []
post_format: []
---
```
<pre class="line-numbers prism-highlight" data-start="1">```javascript
export default {
    mounted() {
        let self = this;
        // 等待被动触发 才能进行初始化
        <span class="katex math inline">nuxt.</span>once('init', (resultData) => {
            // <span class="katex math inline">router 获取路由对象，控制页面跳转
            self.</span>router.push({path: '/home/info'});

            // <span class="katex math inline">route 接受路由对象，接受传参
            console.log(self.</span>route.path);
        })
    }
}

```
```