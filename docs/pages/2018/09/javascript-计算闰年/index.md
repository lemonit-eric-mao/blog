---
title: "Javascript 计算闰年"
date: "2018-09-06"
categories: 
  - "javascript"
---

### 计算闰年

```javascript
var years = [];
for (let i = 2009; i <= new Date().getFullYear(); i++) {
    years.push(i);
}
var months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];
var days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28];

function isLeapYear(year) {
    return (year % 400 == 0) || (year % 4 == 0 && year % 100 != 0);
}

// 生成年
// 生成月
// 根据年月生成天
function generateDayByYearMonth(year, month) {

    let day = [];

    if ([1, 3, 5, 7, 8, 12].includes(month)) {
        day = days.concat(...[29, 30, 31]);
    } else if ([4, 6, 9, 11].includes(month)) {
        day = days.concat(...[29, 30]);
    } else {
        day = (isLeapYear(year)) ? days.concat(29) : days;
    }
    return day;
}
```
