---
title: 'JavaScript 实现 HTML 打印'
date: '2020-03-01T02:49:23+00:00'
status: publish
permalink: /2020/03/01/javascript-%e5%ae%9e%e7%8e%b0-html-%e6%89%93%e5%8d%b0
author: 毛巳煜
excerpt: ''
type: post
id: 5271
category:
    - JavaScript
tag: []
post_format: []
---
```
<pre data-language="HTML">```markup



<div id="wrap">
    
    <div id="printInfo">
        要打印的信息
    </div>
    
    <div>
        <input onclick="doPrint()" type="button" value="打印"></input>
    </div>
</div>

<script type="text/javascript">
    /**
     * &#25171;&#21360;&#25805;&#20316;
     */
    function doPrint() {
        // &#32531;&#23384;&#24403;&#21069;&#39029;&#38754;
        var catchHtml = document.getElementById('wrap').innerHTML;
        // &#35774;&#32622;&#25171;&#21360;&#20869;&#23481;(&#20250;&#26367;&#25442;&#21407;&#26377;&#30340;&#39029;&#38754;)
        window.document.body.innerHTML = document.getElementById('printInfo').innerHTML;
        window.print();
        // &#24674;&#22797;&#24403;&#21069;&#39029;&#38754;
        window.document.body.innerHTML = catchHtml;
    }
</script>

```
```