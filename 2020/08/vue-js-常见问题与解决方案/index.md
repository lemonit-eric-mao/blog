---
title: "Vue.js 常见问题与解决方案"
date: "2020-08-14"
categories: 
  - "vue"
---

* * *

* * *

* * *

###### JS 数据容量单位转换

```javascript
import Vue from 'vue';

class Tools {
    /**
     * 数据容量单位转换
     * @param bytes
     * @returns {string}
     */
    static bytesToSize(bytes) {
        if (bytes === 0) return '0 B';
        let sizes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
        let k = 1024; // or 1000
        let i = Math.floor(Math.log(bytes) / Math.log(k));

        return `${(bytes / Math.pow(k, i)).toPrecision(3)} ${sizes[i]}`;
    }
}

// 添加到 Vue原型链
Vue.prototype.$tools = Tools;

```

* * *

* * *

* * *

###### Vue 监听页面渲染完成

```javascript
// 监听父页面渲染完成后在触发
this.$parent.$nextTick(() => {
    console.log('父页面渲染完成');
});

// 监听自己页面渲染完成后在触发
this.$nextTick(() => {
    console.log('自己页面渲染完成');
});
```

* * *

* * *

* * *

###### 封装node.js 原生事件实现Vue全局emit $globalEmit.js

```javascript
import Vue from 'vue'

/**
 * node.js 原生事件
 */
import {EventEmitter} from 'events'

// 添加到 Vue原型链
Vue.prototype.$GlobalEmit = new EventEmitter();

/**
 * 使用方法：
 *
 * this.eventEmitter.on(eventName, callback);
 *
 * this.eventEmitter.emit(eventName, callback);
 *
 */

```

* * *

* * *

* * *

##### Vue.js 自定义组件怎么用 v-model 传值？

**父组件中绑定`v-model`, 相当于`v-bind:value="value"` 加 `v-on:input="$event.target.value"`， 但这个做法不应该常用， 因为在Vue.js中父子组件传值，按照官方规范要求是单向的，并不建议使用双向绑定**

* * *

###### 子组件模块，以富文本为例

```javascript
<template>
    <section>
        <!-- 这里的value为关键字-->
        <quill-editor v-model="value"/>
    </section>
</template>

<script>
    import {quillEditor} from 'vue-quill-editor'
    import 'quill/dist/quill.core.css'
    import 'quill/dist/quill.snow.css'
    import 'quill/dist/quill.bubble.css'

    export default {
        components: {
            quillEditor
        },
        props: {
            // 这里的value为关键字
            value: ''
        },
        data() {
            return {}
        }
    }
</script>

<style scoped>
</style>
```

* * *

###### 在其它组件中引用用

```javascript
<template>
    <section>
        <TheQuillEditor ref="text" v-model="testForm.content"/>
    </section>
</template>

<script>
    import TheQuillEditor from './TheQuillEditor.vue';

    export default {
        components: {
            TheQuillEditor
        },
        data() {
            return {
                testForm: {
                    content: '测试内容'
                }
            }
        }
    }
</script>

<style scoped>
</style>
```

* * *

* * *

* * *

###### Vue.js + ElementUI 日期格式化

```javascript
<template>
......
        <el-table-column align="center" label="创建时间" prop="create_time" :formatter="dateFormat"/>
......
</template>

<script>

    import moment from 'moment'

    /**
     * 表格
     *
     * @date 2020-02-25
     * @author Eric.Mao
     */
    export default {
        name: 'InventoryListTable',
        methods: {
            /**
             * 日期格式化
             */
            dateFormat(row, column, cellValue, index) {
                if (!cellValue)
                    return '';
                return moment(cellValue).format("YYYY年MM月DD日 HH时mm分ss秒");
            },
        }
    }
</script>
<style scoped>
</style>

```

* * *

* * *

* * *

##### 解决Vue.js项目打包后，基于Node.js的Express服务器发布后, 刷新页面404问题

###### **[Vue Router官方详解](https://router.vuejs.org/zh/guide/essentials/history-mode.html#%E5%9F%BA%E4%BA%8E-node-js-%E7%9A%84-express "Vue Router官方详解")**

###### **[插件用法](https://github.com/bripkens/connect-history-api-fallback#usage "插件用法")**

* * *

###### app.js

```ruby
// 加入history插件，解决刷新页面404问题
const history = require('connect-history-api-fallback');
const bodyParser = require('body-parser');
const express = require('express');
const logger = require('morgan');
const path = require('path');

// 模块引入
const index = require('./routes/index');

const app = express();

// history插件与express一起使用
app.use(history());

// 设置跨域访问
app.all('*', function (req, res, next) {
    res.header("Access-Control-Allow-Origin", "*");
    res.header("Access-Control-Allow-Headers", "Content-Type,Content-Length, Authorization, Accept,X-Requested-With");
    res.header("Access-Control-Allow-Methods", "PUT,POST,GET,DELETE,OPTIONS");
    res.header("X-Powered-By", ' 3.2.1')
    next();
});

/*******************************************/
// 将html的渲染路径直接 指向dist 这样就方便多了
app.use(express.static(path.join(__dirname, '/dist')));
/*******************************************/
app.use(logger('dev'));
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

app.use('/', index);

module.exports = app;
```
