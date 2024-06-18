---
title: 'MySQL 事务隔离级别'
date: '2019-12-30T12:54:37+00:00'
status: publish
permalink: /2019/12/30/mysql-%e4%ba%8b%e5%8a%a1%e9%9a%94%e7%a6%bb%e7%ba%a7%e5%88%ab
author: 毛巳煜
excerpt: ''
type: post
id: 5209
category:
    - MySQL
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### 事务隔离级别

- **脏读**：  
   脏读就是指当事务A对数据进行了修改，而这种修改还没有提交到数据库中，这时，另外一个事务B也访问这个数据，然后使用了这个数据。  
   例如: 有`A、B`两个事务，`A` 事务更新了一份数据，`B` 事务在此时读取了同一份数据，由于某些原因，`A` 事务执行了`rollback`操作，则 `B` 读取数据就会出现不正确的数据。
- **不可重复读**：  
   不可重复读是指在`事务1`内，读取了一条数据，`事务1`还没有结束时，`事务2`也访问了这条数据，修改了这条数据，并提交。紧接着，`事务1`又读这条数据。由于`事务2`的修改，那么`事务1`两次读到的数据可能是不一样的，因此称为是`不可重复读`。
- **幻读**：  
   所谓幻读，指的是当某个事务在读取某个范围内的记录时，另外一个事务又在该范围内插入了新的记录，当之前的事务再次读取该范围的记录时，会产生幻行。  
   例如: 有一个事务查询了几列数据，而另一个事务却在此时插入了几列新的数据，先前事务在接下来的查询中，就会发现有几列数据，先前的事务在接下来的查询中，就会发现有几列数据是它先前所没有的。
- **`注意`**：  
   **不可重复读**和**幻读**的区别是, 前者是指读到了已经提交的事务的 **`更改数据（修改或删除）`** ，后者是指读到了其他已经提交事务的 **`新增数据`** 。  
   对于这两种问题解决采用不同的办法，防止读到更改数据，只需对操作的数据添加  
  **`行级锁`** ，防止操作中的数据发生变化；而防止读到新增数据，往往需要添加 **`表级锁`** ，将整张表锁定，防止新增数据

- - - - - -

**SQL 标准定义了四个隔离级别**

<table><thead><tr><th align="center">**隔离级别** `IsolationLevel`</th><th align="left">**隔离级别** `IsolationLevel`</th><th align="center">**脏写** `DirtyWrite`</th><th align="center">**脏读** `DirtyRead`</th><th align="center">**不可重复读** `FuzzyRead`</th><th align="center">**幻读** `Phantom`</th><th align="left">**解释**</th></tr></thead><tbody><tr><td align="center">**读未提交**</td><td align="left">READ-UNCOMMITTED</td><td align="center">`×`</td><td align="center">√</td><td align="center">√</td><td align="center">√</td><td align="left"> `最低的隔离级别`，允许读取尚未提交的数据变更，可能会导致脏读、幻读或不可重复读</td></tr><tr><td align="center">**读已提交**</td><td align="left">READ-COMMITTED</td><td align="center">`×`</td><td align="center">`×`</td><td align="center">√</td><td align="center">√</td><td align="left"> 允许读取并发事务已经提交的数据，可以阻止脏读，但是幻读或不可重复读仍有可能发生</td></tr><tr><td align="center">**可重复读**</td><td align="left">REPEATABLE-READ</td><td align="center">`×`</td><td align="center">`×`</td><td align="center">`×`</td><td align="center">√</td><td align="left"> 对同一字段的多次读取结果都是一致的，除非数据是被本身事务自己所修改，可以阻止脏读和不可重复读，但幻读仍有可能发生</td></tr><tr><td align="center">**串行化**</td><td align="left">SERIALIZABLE</td><td align="center">`×`</td><td align="center">`×`</td><td align="center">`×`</td><td align="center">`×`</td><td align="left"> `最高的隔离级别`，完全服从ACID的隔离级别。所有的事务依次逐个执行，这样事务之间就完全不可能产生干扰，也就是说，该级别可以防止脏读、不可重复读以及幻读。</td></tr></tbody></table>

- - - - - -

 MySQL InnoDB 存储引擎的默认支持的隔离级别是 `REPEATABLE-READ`（可重复读）, 我们可以通过命令来查看。

###### 查看全局 事务隔离级别

```sql
SELECT @@GLOBAL.tx_isolation;
+-----------------------+
| @@GLOBAL.tx_isolation |
+-----------------------+
| REPEATABLE-READ       |
+-----------------------+
1 row in set (0.01 sec)

```

###### 查看会话级别 事务隔离级别

```sql
SELECT @@tx_isolation;
+-----------------+
| @@tx_isolation  |
+-----------------+
| REPEATABLE-READ |
+-----------------+
1 row in set (0.00 sec)

```

###### 设置全局 事务隔离级别

```sql
SET GLOBAL transaction isolation level REPEATABLE READ;
Execute success (0.01 sec)

```

###### 设置会话级别 事务隔离级别

```sql
SET transaction isolation level REPEATABLE READ;
Execute success (0.01 sec)

```

- - - - - -

- - - - - -

- - - - - -

##### 事务传播方式

<table><thead><tr><th>方式</th><th>说明</th></tr></thead><tbody><tr><td>**PROPAGATION\_`REQUIRED`**</td><td>如果当前没有事务，就新建一个事务，如果已经存在一个事务中，加入到这个事务中</td></tr><tr><td>**PROPAGATION\_`NOT_SUPPORTED`**</td><td>以非事务方式执行操作，如果当前存在事务，就把当前事务挂起，容器不为这个方法开启事务</td></tr><tr><td>**PROPAGATION\_`REQUIRES_NEW`**</td><td>开启一个新事物,如果原本方法存在事务则挂起等待该事务结束,在执行其他事务</td></tr><tr><td>**PROPAGATION\_`MANDATORY`**</td><td>必须在一个事务中进行,否则抛出异常</td></tr><tr><td>**PROPAGATION\_`NEVER`**</td><td>必须在无事务中进行,否则跑出异常</td></tr><tr><td>**PROPAGATION\_`SUPPORTS`**</td><td>有事务就用,没有就不用</td></tr></tbody></table>

- - - - - -

- - - - - -

- - - - - -