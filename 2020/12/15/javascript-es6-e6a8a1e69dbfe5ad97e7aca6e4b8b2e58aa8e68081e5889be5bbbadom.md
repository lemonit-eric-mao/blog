---
title: 'Javascript ES6 模板字符串动态创建DOM'
date: '2020-12-15T05:18:24+00:00'
status: private
permalink: /2020/12/15/javascript-es6-%e6%a8%a1%e6%9d%bf%e5%ad%97%e7%ac%a6%e4%b8%b2%e5%8a%a8%e6%80%81%e5%88%9b%e5%bb%badom
author: 毛巳煜
excerpt: ''
type: post
id: 6648
category:
    - JavaScript
tag: []
post_format: []
---
```
<pre data-language="HTML">```markup

<input onclick="openDialog()" type="button" value="测试弹窗"></input>

<div class="dl-foundation" id="foundation">
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
</div>


```
```

- - - - - -

```javascript
    function openDialog() {
        let dialog = `
            
            <div class="dl-dialog" onclick="recovery(this)">
                
                <div class="dl-title">
                    <div class="dl-text">标题栏</div>
                    <div>
                        
                        <svg class="icon" height="20px" onclick="minimize(this)" version="1.1" viewbox="0 0 1024 1024" width="20px" xmlns="http://www.w3.org/2000/svg">
                            <path d="M76.8 563.2h819.2a51.2 51.2 0 0 0 0-102.4h-819.2a51.2 51.2 0 0 0 0 102.4z" fill="#333333"></path>
                        </svg>
                    </div>
                </div>
                
                <div class="dl-content">正文</div>
                
                <div class="dl-buttons">
                    <div>关闭</div>
                    <div>确定</div>
                </div>
            </div>
        `;

        // 必须要创建一个DOM元素，才能在下面使用appendChild()追加
        let wrapper = document.createElement('div');
        wrapper.classList.add('dl-wrapper');
        // 将模板内容追加到DOM元素
        wrapper.innerHTML = dialog;
        // 获取这个DOM元素内的，子元素并动态设置背景色
        wrapper.querySelector('.dl-content').style.backgroundColor = `#${Math.floor(Math.random() * 0xffffff).toString(16)}`;

        // 最终将DOM元素放到哪里
        let foundation = document.getElementById('foundation');
        // appendChild(这里必须是个DOM对象)
        foundation.appendChild(wrapper);
    }


```