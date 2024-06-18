---
title: 'JavaScript 防抖'
date: '2021-01-11T02:08:19+00:00'
status: private
permalink: /2021/01/11/javascript-%e9%98%b2%e6%8a%96
author: 毛巳煜
excerpt: ''
type: post
id: 6770
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
```
  防抖，指的是无论某个动作被连续触发多少次，直到这个连续动作停止触发后才开始计时延迟，达到延时时间后，才会被当作一次来执行
  比如一个输入框接受用户不断输入，输入结束后才开始搜索

```

- - - - - -

```javascript



    <meta charset="UTF-8"></meta>
    <title>测试防抖</title>


测试连续输入：
<input id="testId" value=""></input>
<script>

    class Debounce {

        constructor(time) {
            this.timeoutId = null;
            // 2&#31186;
            this.time = time || 2000;
        }

        existTime() {
            this.timeoutId && clearTimeout(this.timeoutId);
        }

        send(callback) {
            this.existTime();
            this.timeoutId = setTimeout(() => {
                callback();
            }, this.time);
        }
    }

    // &#27979;&#35797;
    const mDebounce = new Debounce();
    const input = document.getElementById('testId');
    input.oninput = function () {
        mDebounce.send(() => {
            console.log(input.value);
        });
    }

</script>



```