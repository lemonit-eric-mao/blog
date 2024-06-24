---
title: "Javascript 精度丢失 案例"
date: "2018-09-14"
categories: 
  - "javascript"
---

#### 精度丢失经典案例

```javascript
mao-siyu@pc:~$ node
> 0.1 + 0.2
0.30000000000000004
>
```

```javascript
> (0.1+0.2).toFixed(1)
'0.3'
>
```
