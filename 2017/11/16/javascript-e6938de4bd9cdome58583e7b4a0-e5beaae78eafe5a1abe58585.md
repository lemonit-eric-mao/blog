---
title: 'JavaScript 操作DOM元素 循环填充'
date: '2017-11-16T10:14:32+00:00'
status: publish
permalink: /2017/11/16/javascript-%e6%93%8d%e4%bd%9cdom%e5%85%83%e7%b4%a0-%e5%be%aa%e7%8e%af%e5%a1%ab%e5%85%85
author: 毛巳煜
excerpt: ''
type: post
id: 82
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - default
---
```
<pre data-language="HTML">```markup



    <meta charset="UTF-8"></meta>
    <title>Title</title>



<div>
    <div id="test" style="position: relative"></div>
</div>

<script>
    const jsonArray = [
        '111111111111111111111',
        '222222222222222222222',
        '333333333333333333333',
        '444444444444444444444',
        '555555555555555555555',
        '666666666666666666666',
        '777777777777777777777',
        '888888888888888888888',
        '999999999999999999999',
        'AAAAAAAAAAAAAAAAA',
        'BBBBBBBBBBBBBBBBBBB',
        'CCCCCCCCCCCCCCCCCC',
        'DDDDDDDDDDDDDDDD',
        'EEEEEEEEEEEEEEEEEEEEEE'
    ];

    // &#23481;&#22120;
    let testObj = document.getElementById('test');

    // &#21019;&#24314;&#23376;&#20803;&#32032;
    const createElement = (text) => {
        let tempDiv = document.createElement('div');
        tempDiv.innerText = text;
        return tempDiv;
    }

    let elementIndex = 0;
    // &#22635;&#20805;&#25968;&#25454;
    const fill = () => {
        if (elementIndex >= jsonArray.length ){
            // &#24490;&#29615;&#22635;&#20805;
            testObj.appendChild(testObj.children[0]);
        } else {
            // &#22635;&#20805;&#25968;&#25454;
            testObj.appendChild(createElement(jsonArray[elementIndex++]));
        }
    }

    let interval = setInterval(fill, 500);

</script>



```
```