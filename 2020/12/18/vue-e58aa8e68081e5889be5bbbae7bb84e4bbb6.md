---
title: 'Vue 动态创建组件'
date: '2020-12-18T02:29:33+00:00'
status: private
permalink: /2020/12/18/vue-%e5%8a%a8%e6%80%81%e5%88%9b%e5%bb%ba%e7%bb%84%e4%bb%b6
author: 毛巳煜
excerpt: ''
type: post
id: 6662
category:
    - vue
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
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
    const vm = vue.<span class="katex math inline">mount();

    // 返回VM
    // 挂载之后vm.</span>el可以访问到真实dom
    return vm
}

// 添加到 Vue原型链
Vue.prototype.$CreateVue = CreateVue;

```

- - - - - -

###### 在main.js中引入

```javascript
// 添加创建虚拟dom插件
import '@/assets/js/$createVue.js';

```

- - - - - -

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
                  dialog.append(this.<span class="katex math inline">CreateVue(TheMappingExec, {}).</span>el);
             }
         }
     }

```