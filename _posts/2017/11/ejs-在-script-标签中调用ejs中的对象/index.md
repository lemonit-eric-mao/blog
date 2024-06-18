---
title: "ejs 在 script 标签中调用ejs中的对象"
date: "2017-11-29"
categories: 
  - "javascript"
---

### 使用ejs 来做服务器端渲染, 其中有些业务需要在 js脚本中用到服务端数据

### 服务器node.js数据

```javascript
const letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
/*问卷表单*/
router.get('/questionnaire/getform', (req, res) => {
    let testData = {
        datas: {
            quesTitle: "问卷标题,
            quesDescr: "问卷描述",
            problems: [
                {
                    title: "11111111111111111111",
                    radio: "1",
                    options: [
                        "111111",
                        "2222222",
                        "444"
                    ]
                }
            ]
        }
    }
    res.render('questionnaire', {resultData: testData.datas, letters: letters});
});
```

### 对象转换

```javascript
// 将ejs中的对象 转为普通的js的对象
let prob = JSON.parse('<%- JSON.stringify(problems) %>');
```
