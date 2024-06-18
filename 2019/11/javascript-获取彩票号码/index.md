---
title: "Javascript 获取彩票号码"
date: "2019-11-13"
categories: 
  - "javascript"
---

[双色球走势图](http://zst.aicai.com/ssq/ "双色球走势图") 这个网址的走势图比较简单，因为它没有分页好抓取

```javascript
var trs = document.querySelectorAll('#tdata > tr');
var rows = [];
for (let i = 0, len = trs.length; i < len; i++) {

    var tds = trs[i].querySelectorAll('td');
    var column = '';
    for (let j = 0, len = tds.length; j < len; j++) {
        if(tds[j].className == 'c_fbf5e3 bd_rt_a') {
            column += tds[j].innerText + '    ';
        } else if(tds[j].className == 'chartBall01' || tds[j].className == 'chartBall02') {
            column += tds[j].innerText + ' ';
        }
    }
    rows.push(column)
}


for(let k = 0; k < rows.length; k++) {
    console.log(rows[k])
}
```
