---
title: "JavaScript 日期、时间、计算、格式化"
date: "2023-05-18"
categories: 
  - "javascript"
---

### 常用格式函数

```javascript
new Date().toLocaleDateString()
'2024/4/11'

new Date().toLocaleTimeString()
'09:52:16'

new Date().toLocaleString()
'2024/4/11 09:51:57'

new Date().toISOString()
'2024-04-11T01:52:56.574Z'

```

* * *

### 获取本月第一天和最后一天

```javascript
// 获取本月第一天
let d = new Date();
d.setDate(1);
d.toLocaleDateString();

// 获取本月最后一天
let d = new Date();
d.setMonth(d.getMonth() + 1)
d.setDate(0);
d.toLocaleDateString();

```

* * *

### 获取某年有多少天

> ```javascript
> /**
>  * 获取某年有多少天
>  *
>  * @param year
>  * @returns {number}
>  */
> function getDaysInYear(year) {
>     const isLeap = (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0;
>     return isLeap ? 366 : 365;
> }
> ```

* * *

### 计算【x年x月 有多少天】

> ```javascript
> /**
>  * 计算【x年x月 有多少天】
>  *
>  * @param year
>  * @param month
>  * @returns {number}
>  */
> function getDaysInMonth(year, month) {
>   // 获取指定月份的天数
>   const daysInMonth = new Date(year, month, 0).getDate();
>   return daysInMonth;
> }
> 
> ```

* * *

### 计算【x月x日 是x年的第几天】

> ```javascript
> /**
>  * 获取【x月x日 是x年的第几天】
>  * calcDays(2, 29, 2024);  输出结果：2月29日是2024年的第60天
>  *
>  * @param month
>  * @param day
>  * @param year
>  * @returns {number} 天数
>  */
> function calcDays(month, day, year) {
>     let date = new Date(year, month - 1, day);
>     let days = Math.ceil((date - new Date(year, 0, 1)) / (1000 * 60 * 60 * 24)) + 1;
> 
>     console.log(`${month}月${day}日是${year}年的第${days}天`);
>     return days
> }
> ```
> 
> ```javascript
> /**
>  * 获取【x月x日 是x年的第几天】
>  * calcDays('2024-02-29');  输出结果：2024年2月29日是第60天
>  *
>  * @param month
>  * @param day
>  * @param year
>  * @returns {number} 天数
>  */
> function calcDays(dateTimeString) {
>     // 解析日期时间字符串为 Date 对象
>     let date = new Date(dateTimeString);
> 
>     // 获取年份、月份和日期
>     let year = date.getFullYear();
>     let month = date.getMonth() + 1; // 月份从 0 到 11
>     let day = date.getDate();
> 
>     let newDate = new Date(year, month - 1, day);
>     let days = Math.ceil((newDate - new Date(year, 0, 1)) / (1000 * 60 * 60 * 24)) + 1;
> 
>     console.log(`${year}年${month}月${day}日是第${days}天`);
>     return days
> }
> ```

* * *

### 计算【x年的第几天 是x月x日】

> ```javascript
> /**
>  * 计算【x年的第几天 是x月x日】
>  * calcDate(60, 2024);  输出结果：2024年的第60天是2024年2月29日
>  *
>  * @param day 天数
>  * @param year
>  * @returns {string} x年x月x日
>  */
> function calcDate(day, year) {
>     // 设置为该年的 1 月 1 日
>     let date = new Date(year, 0, 1);
>     // 加上相应的天数
>     date.setDate(date.getDate() + day - 1);
> 
>     // 日期格式化样式
>     let options = {year: 'numeric', month: 'long', day: 'numeric', weekday: 'long'};
>     // 日期格式化
>     let dateString = date.toLocaleDateString('zh-CN', options);
> 
>     console.log(`${year}年的第${day}天是${dateString}`);
>     return dateString
> }
> ```

* * *

### JavaScript 时间戳计算时差

> ```javascript
> // 记录起始时间
> const startTime = new Date();
> setTimeout(() => {
>   // 记录结束时间
>   const endTime = new Date();
>   // 日期相减 直接获得时间戳
>   let newTime = endTime - startTime;
>   // 输出时间戳
>   console.log(newTime)
>   // 以毫秒单位表示的差值时间
>   let nDay = Math.floor(newTime / (1000 * 60 * 60 * 24)); // 天
>   let nHour = Math.floor(newTime / (1000 * 60 * 60)) % 24; // 小时
>   let nMinute = Math.floor(newTime / (1000 * 60)) % 60; // 分钟
>   let nSeconds = Math.floor(newTime / 1000) % 60; // 秒
>   // 输出结果
>   console.log(`${nDay} ${nHour} ${nMinute} ${nSeconds}`);
> }, 2000);
> 
> ```

* * *

### JavaScript 计算时间加减

> ```javascript
> let date = new Date('2018-01-31');
> console.log('oldDate:    ' + date.toISOString().slice(0, 10));
> // 在当前日期上减去或加上 (年数, 月数, 天数)
> date.setFullYear(date.getFullYear(), date.getMonth() + 1, date.getDate())
> console.log('newDate:    ' + date.toISOString().slice(0, 10));
> ```
