---
title: 'MySQL REPLACE INTO 用法'
date: '2020-01-06T03:40:48+00:00'
status: publish
permalink: /2020/01/06/mysql-replace-into-%e7%94%a8%e6%b3%95
author: 毛巳煜
excerpt: ''
type: post
id: 5216
category:
    - MySQL
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 一、MySQL 中 replace into的用法，是insert into的增强版。

**`replace into`在向表中插入数据时：**

1. 首先判断数据是否存在。
2. 如果不存在，则插入。
3. 如果存在，则更新。

**`replace into` 跟 `insert` 功能类似，不同点在于:**

1. 表必须有主键或者是唯一索引,否则没有什么不同；
2. 如果有主键或者是唯一索引，则REPLACE`发现重复`的`先删除再插入`，  
  如果记录有多个字段，在插入的时候如果有的字段没有赋值，那么新插入的记录这些字段为空，且返回的值为删除的条数和插入的条数之和；**而insert 发现重复的则报错**。

 **要注意的是：**插入数据的表必须有主键或者是唯一索引！否则的话，`replace into 会直接插入数据`，这将导致表中出现`重复的数据`。

- - - - - -

- - - - - -

- - - - - -

##### 二、MySQL REPLACE INTO 有三种形式：

1. REPLACE INTO  
  **语法：**  
  `REPLACE INTO tbl_name(col_name, ...) VALUES(...)`  
  **说明：**  
  这种形式类似于`INSERT INTO` 的用法

- - - - - -

2. REPLACE INTO SELECT  
  **语法：**  
  `REPLACE INTO tbl_name(col_name, ...) SELECT ...`  
  **说明：**  
  `REPLACE SELECT` 的用法也类似于 `INSERT SELECT` ，这种用法`并不一定要求列名匹配`，事实上，MYSQL甚至`不关心`SELECT`返回的列名`，`它需要的是列的位置`。  
  **例子:**

```sql
REPLACE INTO tb1(  name, title, mood) SELECT  rname, rtitle, rmood from tb2;

```

这个例子使用`REPLACE INTO`从 `tb2`中将所有数据导入`tb1`中。

- - - - - -

3. REPLACE INTO SET  
  **语法：**  
  `REPLACE INTO tbl_name SET col_name=value, ...`  
  **说明：**  
  用法类似于`UPDATE SET`用法，使用一个例如`SET col_name = col_name + 1`的赋值，则对位于右侧的列名称的引用会被作为`DEFAULT(col_name)`处理。因此，该赋值相当于`SET col_name = DEFAULT(col_name) + 1`。

 前两种形式用的多些。其中 `INTO` 关键字可以省略，不过最好加上 `INTO`，这样意思更加直观。另外，对于那些没有给予值的列，MySQL 将自动为这些列赋上默认值。

- - - - - -

- - - - - -

- - - - - -

[原文链接](https://blog.csdn.net/weixin_33736832/article/details/89797070 "原文链接")