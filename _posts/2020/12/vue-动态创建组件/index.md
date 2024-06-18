---
title: "Vue 动态创建组件"
date: "2020-12-18"
categories: 
  - "vue"
---

###### src/assets/js/$createVue.js

```javascript
import Vue from 'vue'

/**
 * 参照文档： https://www.cnblogs.com/guojiabing/p/12805735.html
 * @param Component
 * @param props
 * @returns {*}
 * @constructor
 */
function CreateVue(Component, props) {
    // new Vue({render() {}}),在render中把Component作为根组件
    const vue = new Vue({
        // h是createElement函数，它可以返回虚拟dom
        render(h) {
            // 将Component作为根组件渲染出来
            // h(标签名称或组件配置对象，传递属性、事件等，孩子元素)
            return h(Component, {props})
        }
    });
    // 挂载是为了把虚拟dom变成真实dom
    // 不挂载就没有真实dom
    const vm = vue.$mount();

    // 返回VM
    // 挂载之后vm.$el可以访问到真实dom
    return vm
}

// 添加到 Vue原型链
Vue.prototype.$CreateVue = CreateVue;
```

* * *

###### 在main.js中引入

```javascript
// 添加创建虚拟dom插件
import '@/assets/js/$createVue.js';
```

* * *

###### 使用方法:

```javascript
 // 引用要动态创建的组件
 import TheMappingExec from '@/components/common/TheMappingExec.vue';

    /**
     * 对话框
     *
     * @date 2020-12-17
     * @author Eric.Mao
     */
     export default {
         name: 'TheDialog',
         components: {
             TheMappingExec
         },
         methods: {
             openDialog() {
                  let dialog = document.createElement('div');
                  dialog.append(this.$CreateVue(TheMappingExec, {}).$el);
             }
         }
     }
```
