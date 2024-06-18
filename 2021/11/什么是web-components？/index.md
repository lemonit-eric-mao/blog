---
title: "什么是Web Components？"
date: "2021-11-24"
categories: 
  - "前端开发"
---

###### **[Web Components 入门实例教程](http://www.ruanyifeng.com/blog/2019/08/web_components.html "Web Components 入门实例教程")**

###### **[MDN文档 Web Components](https://developer.mozilla.org/zh-CN/docs/Web/Web_Components "MDN文档 Web Components")**

* * *

* * *

* * *

###### 自定义标签元素

```javascript
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>JS Bin</title>
</head>
<body>
<!--1. 创建一个自定义标签元素-->
<user-card></user-card>
<!--2. 自定义元素的类-->
<script>
    /**
     * 自定义元素的类
     * 注意，这个类的父类是HTMLElement，因此继承了 HTML 元素的特性。
     */
    class UserCard extends HTMLElement {
        constructor() {
            super();

            let image = document.createElement('img');
            image.src = 'https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png';
            image.classList.add('image');

            let container = document.createElement('div');
            container.classList.add('container');

            let name = document.createElement('p');
            name.classList.add('name');
            name.innerText = 'User Name';

            let email = document.createElement('p');
            email.classList.add('email');
            email.innerText = 'yourmail@some-email.com';

            let button = document.createElement('button');
            button.classList.add('button');
            button.innerText = 'Follow';

            container.append(name, email, button);
            this.append(image, container);
        }
    }

    // 3. 使用浏览器原生的customElements.define()方法，告诉浏览器<user-card>元素与这个类关联。
    window.customElements.define('user-card', UserCard);
</script>

</body>
</html>
```

* * *

* * *

* * *

###### 使用 HTML template

```javascript
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>JS Bin</title>
</head>
<body>

<!--1. 创建一个自定义标签元素-->
<user-card></user-card>

<!--2. 使用<template>标签，在它里面使用 HTML 自定义 DOM。-->
<template id="userCardTemplate">
    <img src="https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png" class="image">
    <div class="container">
        <p class="name">User Name</p>
        <p class="email">yourmail@some-email.com</p>
        <button class="button">Follow</button>
    </div>
</template>

<!--3. 自定义元素的类-->
<script>
    /**
     * 自定义元素的类
     * 注意，这个类的父类是HTMLElement，因此继承了 HTML 元素的特性。
     */
    class UserCard extends HTMLElement {
        /**
         * 代码中，获取<template>节点以后，克隆了它的所有子元素，
         * 这是因为可能有多个自定义元素的实例，这个模板还要留给其他实例使用，所以不能直接移动它的子元素。
         */
        constructor() {
            super();
            // 为自定义元素加载<template>
            let templateElem = document.getElementById('userCardTemplate');
            // 克隆了<template>的所有子元素
            let content = templateElem.content.cloneNode(true);
            this.appendChild(content);
        }
    }

    // 4. 使用浏览器原生的customElements.define()方法，告诉浏览器<user-card>元素与这个类关联。
    window.customElements.define('user-card', UserCard);
</script>

</body>
</html>
```

* * *

* * *

* * *

###### ShadowDOM 影子模式

```markup
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width">
    <title>JS Bin</title>
    <style>
        #app {
            border: red 1px solid;
            display: flex;
        }
    </style>
</head>
<body>

<div id="app">
    <!--1. 创建一个自定义标签元素-->
    <user-card></user-card>
</div>

<!--2. 使用<template>标签，在它里面使用 HTML 自定义 DOM。-->
<template id="userCardTemplate">
    <style>
        #app {
            border: blue 1px solid;
        }
    </style>
    <div class="container">
        <div id="app">
            <img src="https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png" class="image">
            <p class="name">User Name</p>
            <p class="email">yourmail@some-email.com</p>
            <button class="button">Follow</button>
        </div>
    </div>
</template>

<!--3. 自定义元素的类-->
<script>
    /**
     * 自定义元素的类
     * 注意，这个类的父类是HTMLElement，因此继承了 HTML 元素的特性。
     */
    class UserCard extends HTMLElement {
        /**
         * 代码中，获取<template>节点以后，克隆了它的所有子元素，
         * 这是因为可能有多个自定义元素的实例，这个模板还要留给其他实例使用，所以不能直接移动它的子元素。
         */
        constructor() {
            super();

            // this.attachShadow()方法的参数{ mode: 'open' }，表示 Shadow DOM 是开启的，允许外部访问。
            // this.attachShadow()方法的参数{ mode: 'closed' }，表示 Shadow DOM 是封闭的，不允许外部访问。
            let shadow = this.attachShadow({mode: 'closed'});

            // 为自定义元素加载<template>
            let templateElem = document.getElementById('userCardTemplate');
            // 克隆了<template>的所有子元素
            let content = templateElem.content.cloneNode(true);

            // this.appendChild(content);
            shadow.appendChild(content);
        }
    }

    // 4. 使用浏览器原生的customElements.define()方法，告诉浏览器<user-card>元素与这个类关联。
    window.customElements.define('user-card', UserCard);
</script>

</body>
</html>

```

* * *

* * *

* * *
