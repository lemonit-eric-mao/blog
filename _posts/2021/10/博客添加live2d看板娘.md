---
title: "博客添加live2d看板娘"
date: "2021-10-28"
categories: 
  - "非技术文档"
---

###### wordpress --> 自定义 --> 小工具 --> 自定义html

```javascript
<script src="https://eqcn.ajz.miesnfu.com/wp-content/plugins/wp-3d-pony/live2dw/lib/L2Dwidget.min.js"></script>

<script>

    // "黑猫": "https://unpkg.com/live2d-widget-model-hijiki@1.0.5/assets/hijiki.model.json",
    // "白猫": "https://unpkg.com/live2d-widget-model-tororo@1.0.5/assets/tororo.model.json",
    // "狗狗": "https://unpkg.com/live2d-widget-model-wanko@1.0.5/assets/wanko.model.json",
    // "萌娘": "https://unpkg.com/live2d-widget-model-shizuku@1.0.5/assets/shizuku.model.json",
    // "小可爱1": "https://unpkg.com/live2d-widget-model-z16@1.0.5/assets/z16.model.json",
    // "小可爱2": "https://unpkg.com/live2d-widget-model-koharu@1.0.5/assets/koharu.model.json"
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
