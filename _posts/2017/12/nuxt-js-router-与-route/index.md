---
title: "Nuxt.js $router 与 $route"
date: "2017-12-12"
categories: 
  - "vue"
---

```javascript
export default {
    mounted() {
        let self = this;
        // 等待被动触发 才能进行初始化
        $nuxt.$once('init', (resultData) => {
            // $router 获取路由对象，控制页面跳转
            self.$router.push({path: '/home/info'});

            // $route 接受路由对象，接受传参
            console.log(self.$route.path);
        })
    }
}
```
