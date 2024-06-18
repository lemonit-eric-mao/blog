---
title: "JavaScript 欺骗词法"
date: "2017-11-16"
categories: 
  - "javascript"
---

##### 欺骗词法

  JavaScript 引擎会在编译阶段进行数项的性能优化， 但如果引擎在代码中发现了 **`eval`** 或 **`with`** , 它只能简单地 **`假设`** 关于标识符位置的判断都是 **`无效`** 的，因为 **`引擎`** 无法在**词法分析阶**段明确知道这些代码会如何对作用域进行修改， 所有的优化**可能都是无意义**的， 所以 **`引擎`** 最简单的做法就是 **`完全不做任何优化`** 。

  如果代码中大量使用 **`eval`** 或 **`with`** ，那么运行起来一定会变得非常慢。

##### 小结

JavaScript 中有两个机制可以 **`欺骗`** 词法作用域 **`eval`** 或 **`with`**

**`eval(...)`** 可以对一段包含一个或多个声明的 **`代码`** 字符串进行演算， 并在程序运行时借此来 **`修改它所处的词法作用域`**

###### **with**

**`with`** 关键字，实际上是根据你传递给它的对象，凭空创建了一个 **`全新的词法作用域`** ， 同样是在运行时

* * *

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
    return Function(`return (${funName})`)();
}
dynamicFun('Test.mMethod')()
// Log: mMethod方法被执行, 参数为undefined

///////////////////////////////////////////////////////

// Function 方法2 形参写法
function dynamicFun(funName, ... param){
    return Function(`return (${funName})`)(param);
}
dynamicFun('Test.mMethod')('aaa')
// Log: mMethod方法被执行, 参数为aaa
```

* * *

* * *

* * *

###### 在ts中的写法

```javascript
<script lang="ts">
    import {Component, Vue} from 'vue-property-decorator'

    @Component({})
    export default class TheUserInfo extends Vue {

        /**
         * 声明当前对象以索引方式执行时的类型
         * 作用： this[限定这里的类型为string类型]
         * this_index 只起到占位的作用，非关键字符，任意写。
         * 解决声明时引发的异常
         * TS7053: Element implicitly has an 'any' type because expression of type 'string' can't be used to index type 'TheUserInfo'.
         *   No index signature with a parameter of type 'string' was found on type 'TheUserInfo'.
         */
        [this_index: string]: any

        constructor() {
            super();
            this.handleMethod('logout');
        }

        /**
         * 退出
         */
        handleMethod(command: string) {
            this[command]();
        }

        logout() {
            console.log('退出');
        }
    }
</script>
```
