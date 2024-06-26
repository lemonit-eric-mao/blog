---
title: "JavaScript 实现 HTML 打印"
date: "2020-03-01"
categories: 
  - "javascript"
---

```markup
<head>
</head>
<body>
<div id="wrap">
    <!--start-print-->
    <div id="printInfo">
        要打印的信息
    </div>
    <!--end-print-->
    <div>
        <input onClick="doPrint()" type="button" value="打印"/>
    </div>
</div>
</body>
<script type="text/javascript">
    /**
     * 打印操作
     */
    function doPrint() {
        // 缓存当前页面
        var catchHtml = document.getElementById('wrap').innerHTML;
        // 设置打印内容(会替换原有的页面)
        window.document.body.innerHTML = document.getElementById('printInfo').innerHTML;
        window.print();
        // 恢复当前页面
        window.document.body.innerHTML = catchHtml;
    }
</script>
</html>

```
