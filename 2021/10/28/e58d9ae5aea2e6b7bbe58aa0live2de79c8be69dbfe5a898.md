---
title: 博客添加live2d看板娘
date: '2021-10-28T06:03:43+00:00'
status: private
permalink: /2021/10/28/%e5%8d%9a%e5%ae%a2%e6%b7%bb%e5%8a%a0live2d%e7%9c%8b%e6%9d%bf%e5%a8%98
author: 毛巳煜
excerpt: ''
type: post
id: 8056
category:
    - 自学整理
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### wordpress --&gt; 自定义 --&gt; 小工具 --&gt; 自定义html

```javascript
<script src="https://eqcn.ajz.miesnfu.com/wp-content/plugins/wp-3d-pony/live2dw/lib/L2Dwidget.min.js"></script>

<script>

    // "&#40657;&#29483;": "https://unpkg.com/live2d-widget-model-hijiki@1.0.5/assets/hijiki.model.json",
    // "&#30333;&#29483;": "https://unpkg.com/live2d-widget-model-tororo@1.0.5/assets/tororo.model.json",
    // "&#29399;&#29399;": "https://unpkg.com/live2d-widget-model-wanko@1.0.5/assets/wanko.model.json",
    // "&#33804;&#23064;": "https://unpkg.com/live2d-widget-model-shizuku@1.0.5/assets/shizuku.model.json",
    // "&#23567;&#21487;&#29233;1": "https://unpkg.com/live2d-widget-model-z16@1.0.5/assets/z16.model.json",
    // "&#23567;&#21487;&#29233;2": "https://unpkg.com/live2d-widget-model-koharu@1.0.5/assets/koharu.model.json"
    const urls = [
        "https://unpkg.com/live2d-widget-model-hijiki@1.0.5/assets/hijiki.model.json",
        "https://unpkg.com/live2d-widget-model-tororo@1.0.5/assets/tororo.model.json",
        "https://unpkg.com/live2d-widget-model-wanko@1.0.5/assets/wanko.model.json",
        "https://unpkg.com/live2d-widget-model-shizuku@1.0.5/assets/shizuku.model.json",
        "https://unpkg.com/live2d-widget-model-z16@1.0.5/assets/z16.model.json",
        "https://unpkg.com/live2d-widget-model-koharu@1.0.5/assets/koharu.model.json"
    ]

    let i = Math.floor(Math.random() * 6);

    L2Dwidget.init({
        "model": {
            jsonPath: urls[i],
            "scale": 1
        },
        "display": {
            "position": "right",
            "width": 75,
            "height": 150,
            "hOffset": 0,
            "vOffset": -20
        },
        "mobile": {
            "show": true,
            "scale": 0.5
        },
        "react": {
            "opacityDefault": 0.7,
            "opacityOnHover": 0.2
        }
    });
</script>

```