---
title: "Node.js 使用注解"
date: "2022-01-21"
categories: 
  - "node-js"
---

##### 补充知识点

###### 让代码中可以使用注解功能, 需要安插 babel插件

```ruby
npm install -D @babel/plugin-proposal-decorators
```

* * *

###### 在.babelrc配置文件中加入如下配置

```json
{
    "presets": [
        ......
    ],
    "plugins": [
        [
            "@babel/plugin-proposal-decorators",
            {
                "legacy": true
            }
        ]
    ]
}

```

* * *

###### 在任意位置测试类注解使用

```javascript
/**
 * 定义类注解
 */
function isTestable(value) {
    return function decorator(target) {
        target.isTestable = value;
    };
}


/**
 * 使用类注解
 */
@isTestable(true)
class MyClass {
}

/**
 * 测试类注解使用结果
 */
console.log(MyClass.isTestable)

```

* * *

* * *

* * *

##### 包装`koa-router`路由，使用注解进行管理

###### [项目地址](https://gitee.com/eric-mao/koa2-server/tree/decorator-router "项目地址")

```javascript
import KoaRouter from 'koa-router'

export function GET(url) { // 这一层表示的是方法的注解层

    /**
     * 方法的注解就是这种参数格式，它是固定写法
     *
     * @param target
     * @param name 方法名
     * @param descriptor 方法的相关信息
     */
    return function (target, name, descriptor) { // 这一层表示注解所对应的方法的相关信息
        // 1. descriptor.value 是真正的方法，先缓存起来，接下来我们要修改原来的方法
        let fn = descriptor.value
        // 2. 替换原有的方法，(注意：这里只是配置，并没有执行，真正加入到 koa-router 中的操作是在最下面的Controller里面进行的)
        descriptor.value = (router) => {
            console.log(222222)
            // 3. 然后在原有的方法外面加一层路由的配置
            router.get(url, async (ctx, next) => {
                // 4. 最后在调用原来的方法
                await fn(ctx, next)
            })
        }
    }
}

export function POST(url) {
    return function (target, name, descriptor) {
        let fn = descriptor.value
        descriptor.value = (router) => {
            router.post(url, async (ctx, next) => {
                await fn(ctx, next)
            })
        }
    }
}

export function PUT(url) {
    return function (target, name, descriptor) {
        let fn = descriptor.value
        descriptor.value = (router) => {
            router.put(url, async (ctx, next) => {
                await fn(ctx, next)
            })
        }
    }
}

export function DELETE(url) {
    return function (target, name, descriptor) {
        let fn = descriptor.value
        descriptor.value = (router) => {
            router.delete(url, async (ctx, next) => {
                await fn(ctx, next)
            })
        }
    }
}

/**
 * 类注解
 *   类注解在这里只做路由前缀作用
 * @param prefix 配置路由前缀
 * @returns {function(*): *}
 * @constructor
 */
export function Controller(prefix) { // 这一层是类的注解层

    let router = new KoaRouter()

    if (prefix) {
        router.prefix(prefix)
    }

    /**
     * @param target 类对象
     */
    return function (target) {  // 这一层表示注解所对应的类对象的相关信息
        // 获取类中的所有方法
        let reqList = Object.getOwnPropertyDescriptors(target.prototype)
        for (let v in reqList) {
            // 排除类的构造方法
            if (v !== 'constructor') {
                let fn = reqList[v].value
                console.log(111111)
                // 将路由对象传给上面的方法注解配置，将带有注解的方法加入到路由中，完成最后的路由配置
                fn(router)
            }
        }
        return router
    }
}


/**
 * 总结
 * 注解的执行顺序是先执行方法内部的配置
 * 然后在执行类注解内部的配置
 */

```

* * *

* * *

* * *

###### 在app.js中的使用

```javascript
import router from './controller/DemoController'
// 添加路由功能
app.use(router.routes());
app.use(router.allowedMethods());

```

* * *

* * *

* * *

###### 在Controller中的使用

```javascript
import {Controller, GET} from "../commons/annotation/decorator";

@Controller('/demo')
export default class HelloController {

    @GET('/hello')
    async hello(ctx) {
        ctx.body = 'Hello!'
    }

}

```

* * *

* * *

* * *
