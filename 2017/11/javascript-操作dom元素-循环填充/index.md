---
title: "JavaScript 操作DOM元素 循环填充"
date: "2017-11-16"
categories: 
  - "javascript"
---

```markup
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>

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

    // 容器
    let testObj = document.getElementById('test');

    // 创建子元素
    const createElement = (text) => {
        let tempDiv = document.createElement('div');
        tempDiv.innerText = text;
        return tempDiv;
    }

    let elementIndex = 0;
    // 填充数据
    const fill = () => {
        if (elementIndex >= jsonArray.length ){
            // 循环填充
            testObj.appendChild(testObj.children[0]);
        } else {
            // 填充数据
            testObj.appendChild(createElement(jsonArray[elementIndex++]));
        }
    }

    let interval = setInterval(fill, 500);

</script>
</body>
</html>
```
