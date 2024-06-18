---
title: '什么是Web Components？'
date: '2021-11-24T06:41:13+00:00'
status: private
permalink: /2021/11/24/%e4%bb%80%e4%b9%88%e6%98%afweb-components%ef%bc%9f
author: 毛巳煜
excerpt: ''
type: post
id: 8171
category:
    - 前端开发
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### **[Web Components 入门实例教程](http://www.ruanyifeng.com/blog/2019/08/web_components.html "Web Components 入门实例教程")**

###### **[MDN文档 Web Components](https://developer.mozilla.org/zh-CN/docs/Web/Web_Components "MDN文档 Web Components")**

- - - - - -

- - - - - -

- - - - - -

###### 自定义标签元素

```javascript



    <meta charset="utf-8"></meta>
    <meta content="width=device-width" name="viewport"></meta>
    <title>JS Bin</title>



<user-card></user-card>

<script>
    /**
     * &#33258;&#23450;&#20041;&#20803;&#32032;&#30340;&#31867;
     * &#27880;&#24847;&#65292;&#36825;&#20010;&#31867;&#30340;&#29238;&#31867;&#26159;HTMLElement&#65292;&#22240;&#27492;&#32487;&#25215;&#20102; HTML &#20803;&#32032;&#30340;&#29305;&#24615;&#12290;
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

    // 3. &#20351;&#29992;&#27983;&#35272;&#22120;&#21407;&#29983;&#30340;customElements.define()&#26041;&#27861;&#65292;&#21578;&#35785;&#27983;&#35272;&#22120;<user-card>&#20803;&#32032;&#19982;&#36825;&#20010;&#31867;&#20851;&#32852;&#12290;
    window.customElements.define('user-card', UserCard);
</script>




```

- - - - - -

- - - - - -

- - - - - -

###### 使用 HTML template

```javascript



    <meta charset="utf-8"></meta>
    <meta content="width=device-width" name="viewport"></meta>
    <title>JS Bin</title>




<user-card></user-card>


<template id="userCardTemplate">
    <img class="image" decoding="async" src="https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"></img>
    <div class="container">
        <p class="name">User Name</p>
        <p class="email">yourmail@some-email.com</p>
        <button class="button">Follow</button>
    </div>
</template>


<script>
    /**
     * &#33258;&#23450;&#20041;&#20803;&#32032;&#30340;&#31867;
     * &#27880;&#24847;&#65292;&#36825;&#20010;&#31867;&#30340;&#29238;&#31867;&#26159;HTMLElement&#65292;&#22240;&#27492;&#32487;&#25215;&#20102; HTML &#20803;&#32032;&#30340;&#29305;&#24615;&#12290;
     */
    class UserCard extends HTMLElement {
        /**
         * &#20195;&#30721;&#20013;&#65292;&#33719;&#21462;<template>&#33410;&#28857;&#20197;&#21518;&#65292;&#20811;&#38534;&#20102;&#23427;&#30340;&#25152;&#26377;&#23376;&#20803;&#32032;&#65292;
         * &#36825;&#26159;&#22240;&#20026;&#21487;&#33021;&#26377;&#22810;&#20010;&#33258;&#23450;&#20041;&#20803;&#32032;&#30340;&#23454;&#20363;&#65292;&#36825;&#20010;&#27169;&#26495;&#36824;&#35201;&#30041;&#32473;&#20854;&#20182;&#23454;&#20363;&#20351;&#29992;&#65292;&#25152;&#20197;&#19981;&#33021;&#30452;&#25509;&#31227;&#21160;&#23427;&#30340;&#23376;&#20803;&#32032;&#12290;
         */
        constructor() {
            super();
            // &#20026;&#33258;&#23450;&#20041;&#20803;&#32032;&#21152;&#36733;<template>
            let templateElem = document.getElementById('userCardTemplate');
            // &#20811;&#38534;&#20102;<template>&#30340;&#25152;&#26377;&#23376;&#20803;&#32032;
            let content = templateElem.content.cloneNode(true);
            this.appendChild(content);
        }
    }

    // 4. &#20351;&#29992;&#27983;&#35272;&#22120;&#21407;&#29983;&#30340;customElements.define()&#26041;&#27861;&#65292;&#21578;&#35785;&#27983;&#35272;&#22120;<user-card>&#20803;&#32032;&#19982;&#36825;&#20010;&#31867;&#20851;&#32852;&#12290;
    window.customElements.define('user-card', UserCard);
</script>




```

- - - - - -

- - - - - -

- - - - - -

###### ShadowDOM 影子模式

```
<pre data-language="HTML">```markup



    <meta charset="utf-8"></meta>
    <meta content="width=device-width" name="viewport"></meta>
    <title>JS Bin</title>
    <style>
        #app {
            border: red 1px solid;
            display: flex;
        }
    </style>



<div id="app">
    
    <user-card></user-card>
</div>


<template id="userCardTemplate">
    <style>
        #app {
            border: blue 1px solid;
        }
    </style>
    <div class="container">
        <div id="app">
            <img class="image" decoding="async" src="https://www.baidu.com/img/PCtm_d9c8750bed0b3c7d089fa7d55720d6cf.png"></img>
            <p class="name">User Name</p>
            <p class="email">yourmail@some-email.com</p>
            <button class="button">Follow</button>
        </div>
    </div>
</template>


<script>
    /**
     * &#33258;&#23450;&#20041;&#20803;&#32032;&#30340;&#31867;
     * &#27880;&#24847;&#65292;&#36825;&#20010;&#31867;&#30340;&#29238;&#31867;&#26159;HTMLElement&#65292;&#22240;&#27492;&#32487;&#25215;&#20102; HTML &#20803;&#32032;&#30340;&#29305;&#24615;&#12290;
     */
    class UserCard extends HTMLElement {
        /**
         * &#20195;&#30721;&#20013;&#65292;&#33719;&#21462;<template>&#33410;&#28857;&#20197;&#21518;&#65292;&#20811;&#38534;&#20102;&#23427;&#30340;&#25152;&#26377;&#23376;&#20803;&#32032;&#65292;
         * &#36825;&#26159;&#22240;&#20026;&#21487;&#33021;&#26377;&#22810;&#20010;&#33258;&#23450;&#20041;&#20803;&#32032;&#30340;&#23454;&#20363;&#65292;&#36825;&#20010;&#27169;&#26495;&#36824;&#35201;&#30041;&#32473;&#20854;&#20182;&#23454;&#20363;&#20351;&#29992;&#65292;&#25152;&#20197;&#19981;&#33021;&#30452;&#25509;&#31227;&#21160;&#23427;&#30340;&#23376;&#20803;&#32032;&#12290;
         */
        constructor() {
            super();

            // this.attachShadow()&#26041;&#27861;&#30340;&#21442;&#25968;{ mode: 'open' }&#65292;&#34920;&#31034; Shadow DOM &#26159;&#24320;&#21551;&#30340;&#65292;&#20801;&#35768;&#22806;&#37096;&#35775;&#38382;&#12290;
            // this.attachShadow()&#26041;&#27861;&#30340;&#21442;&#25968;{ mode: 'closed' }&#65292;&#34920;&#31034; Shadow DOM &#26159;&#23553;&#38381;&#30340;&#65292;&#19981;&#20801;&#35768;&#22806;&#37096;&#35775;&#38382;&#12290;
            let shadow = this.attachShadow({mode: 'closed'});

            // &#20026;&#33258;&#23450;&#20041;&#20803;&#32032;&#21152;&#36733;<template>
            let templateElem = document.getElementById('userCardTemplate');
            // &#20811;&#38534;&#20102;<template>&#30340;&#25152;&#26377;&#23376;&#20803;&#32032;
            let content = templateElem.content.cloneNode(true);

            // this.appendChild(content);
            shadow.appendChild(content);
        }
    }

    // 4. &#20351;&#29992;&#27983;&#35272;&#22120;&#21407;&#29983;&#30340;customElements.define()&#26041;&#27861;&#65292;&#21578;&#35785;&#27983;&#35272;&#22120;<user-card>&#20803;&#32032;&#19982;&#36825;&#20010;&#31867;&#20851;&#32852;&#12290;
    window.customElements.define('user-card', UserCard);
</script>





```
```

- - - - - -

- - - - - -

- - - - - -