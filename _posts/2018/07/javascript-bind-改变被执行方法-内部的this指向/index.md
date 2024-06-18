---
title: "Javascript .bind() 改变被执行方法 内部的this指向"
date: "2018-07-05"
categories: 
  - "javascript"
---

```javascript
const Demo = {
    objName: 'objName == Demo'
}

class Test {

    constructor() {
        this.objName = 'objName == test';
    }

    foo(callback) {
        // callback(this.show, this.hide);
        callback(this.show.bind(this), this.hide.bind(Demo));
    }

    show() {
        console.log('show');
        console.log(this.objName);
    }

    hide() {
        console.log(this.objName);
        console.log('hide');
    }
}
/**
 * 测试
 */
new Test().foo((show, hide) => {
    show();
    hide();
});

show
objName == test
objName == Demo
hide
```
