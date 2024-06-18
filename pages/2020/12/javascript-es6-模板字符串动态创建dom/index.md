---
title: "Javascript ES6 模板字符串动态创建DOM"
date: "2020-12-15"
categories: 
  - "javascript"
---

```markup
<body>
<input type="button" value="测试弹窗" onclick="openDialog()"/>
<!--地基-->
<div class="dl-foundation" id="foundation">
    <!-- <div class="dl-wrapper">-->
    <!-- <!– 对话框 –>-->
    <!-- <div class="dl-dialog" onclick="recovery(this)">-->
    <!-- <!– 标题栏 –>-->
    <!-- <div class="dl-title">-->
    <!-- <div class="dl-text">标题栏</div>-->
    <!-- <div>-->
    <!-- <!– 最小化–>-->
    <!-- <svg onclick="minimize(this)" class="icon" width="20px" height="20px" viewBox="0 0 1024 1024" version="1.1"-->
    <!-- xmlns="http://www.w3.org/2000/svg">-->
    <!-- <path fill="#333333" d="M76.8 563.2h819.2a51.2 51.2 0 0 0 0-102.4h-819.2a51.2 51.2 0 0 0 0 102.4z"/>-->
    <!-- </svg>-->
    <!-- </div>-->
    <!-- </div>-->
    <!-- <!– 正文 –>-->
    <!-- <div class="dl-content">正文</div>-->
    <!-- <!– 按钮 –>-->
    <!-- <div class="dl-buttons">-->
    <!-- <div>关闭</div>-->
    <!-- <div>确定</div>-->
    <!-- </div>-->
    <!-- </div>-->
    <!-- </div>-->
</div>
</body>
```

* * *

```javascript
    function openDialog() {
        let dialog = `
            <!-- 对话框 -->
            <div class="dl-dialog" onclick="recovery(this)">
                <!-- 标题栏 -->
                <div class="dl-title">
                    <div class="dl-text">标题栏</div>
                    <div>
                        <!-- 最小化-->
                        <svg onclick="minimize(this)" class="icon" width="20px" height="20px" viewBox="0 0 1024 1024" version="1.1"
                             xmlns="http://www.w3.org/2000/svg">
                            <path fill="#333333" d="M76.8 563.2h819.2a51.2 51.2 0 0 0 0-102.4h-819.2a51.2 51.2 0 0 0 0 102.4z"/>
                        </svg>
                    </div>
                </div>
                <!-- 正文 -->
                <div class="dl-content">正文</div>
                <!-- 按钮 -->
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
