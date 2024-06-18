---
title: 'JavaScript 欺骗词法'
date: '2017-11-16T10:11:37+00:00'
status: publish
permalink: /2017/11/16/javascript-%e6%9b%bf%e4%bb%a3eval%e6%96%b9%e6%b3%95
author: 毛巳煜
excerpt: ''
type: post
id: 72
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 欺骗词法

 JavaScript 引擎会在编译阶段进行数项的性能优化， 但如果引擎在代码中发现了 **`eval`** 或 **`with`** , 它只能简单地 **`假设`** 关于标识符位置的判断都是 **`无效`** 的，因为 **`引擎`** 无法在**词法分析阶**段明确知道这些代码会如何对作用域进行修改， 所有的优化**可能都是无意义**的， 所以 **`引擎`** 最简单的做法就是 **`完全不做任何优化`** 。

 如果代码中大量使用 **`eval`** 或 **`with`** ，那么运行起来一定会变得非常慢。

##### 小结

JavaScript 中有两个机制可以 **`欺骗`** 词法作用域 **`eval`** 或 **`with`**

**`eval(...)`** 可以对一段包含一个或多个声明的 **`代码`** 字符串进行演算， 并在程序运行时借此来 **`修改它所处的词法作用域`**

###### **with**

**`with`** 关键字，实际上是根据你传递给它的对象，凭空创建了一个 **`全新的词法作用域`** ， 同样是在运行时

- - - - - -

```javascript
/**
 * 测试
 * @constructor
 */
var Test = function () {
}

Test.mMethod = function (param) {
    console.info("mMethod方法被执行, 参数为" + param);
}

///////////////////////////////////////////////////////

// eval 方法
eval('Test.mMethod("eval1")');
// Log: mMethod方法被执行, 参数为eval1

///////////////////////////////////////////////////////

// Function 方法1 无参写法
function dynamicFun(funName){
    return Function(`return (<span class="katex math inline">{funName})`)();
}
dynamicFun('Test.mMethod')()
// Log: mMethod方法被执行, 参数为undefined

///////////////////////////////////////////////////////

// Function 方法2 形参写法
function dynamicFun(funName, ... param){
    return Function(`return (</span>{funName})`)(param);
}
dynamicFun('Test.mMethod')('aaa')
// Log: mMethod方法被执行, 参数为aaa

```

- - - - - -

- - - - - -

- - - - - -

###### 在ts中的写法

```javascript
<script lang="ts">
    import {Component, Vue} from 'vue-property-decorator'

    @Component({})
    export default class TheUserInfo extends Vue {

        /**
         * &#22768;&#26126;&#24403;&#21069;&#23545;&#35937;&#20197;&#32034;&#24341;&#26041;&#24335;&#25191;&#34892;&#26102;&#30340;&#31867;&#22411;
         * &#20316;&#29992;&#65306; this[&#38480;&#23450;&#36825;&#37324;&#30340;&#31867;&#22411;&#20026;string&#31867;&#22411;]
         * this_index &#21482;&#36215;&#21040;&#21344;&#20301;&#30340;&#20316;&#29992;&#65292;&#38750;&#20851;&#38190;&#23383;&#31526;&#65292;&#20219;&#24847;&#20889;&#12290;
         * &#35299;&#20915;&#22768;&#26126;&#26102;&#24341;&#21457;&#30340;&#24322;&#24120;
         * TS7053: Element implicitly has an 'any' type because expression of type 'string' can't be used to index type 'TheUserInfo'.
         * &nbsp;&nbsp;No index signature with a parameter of type 'string' was found on type 'TheUserInfo'.
         */
        [this_index: string]: any

        constructor() {
            super();
            this.handleMethod('logout');
        }

        /**
         * &#36864;&#20986;
         */
        handleMethod(command: string) {
            this[command]();
        }

        logout() {
            console.log('&#36864;&#20986;');
        }
    }
</script>

```