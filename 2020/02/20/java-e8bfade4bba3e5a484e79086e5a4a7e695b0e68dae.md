---
title: 'Java 迭代处理大数据'
date: '2020-02-20T16:25:30+00:00'
status: private
permalink: /2020/02/20/java-%e8%bf%ad%e4%bb%a3%e5%a4%84%e7%90%86%e5%a4%a7%e6%95%b0%e6%8d%ae
author: 毛巳煜
excerpt: ''
type: post
id: 5261
category:
    - Java
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### 1 清洗一个表中数据到另一个表中，`每次迭代5000条`数据直到获取不到值为止

```java
List<model> resultList;
do {
    Model model = new Model();
    // MySQL语法
    resultList = mapper.selectT1List("SELECT * FROM t1 ORDER BY id ASC LIMIT 5000;");
    // SQL Server语法
    // resultList = mapper.selectT1List("SELECT TOP (5000) * FROM t1 ORDER BY id ASC;");
    // 插入数据到另一个表中;
    // 但因为插入数据会收到数据库自身的限制影响，还需要进一步的迭代插入
    // 临时存放迭代的数据
    List<model> tempList = new ArrayList();
    for (int i = 0; i </model></model>
```

- - - - - -

###### 2 迭代更新`一次最多2000条`, 直到更新完所有符合条件的数据

```java
int result;
do {
    // MySQL语法
    result = mapper.update("UPDATE t1 SET delete_flag = 1 WHERE delete_flag = 0 ORDER BY id ASC LIMIT 2000;");
    // SQL Server语法
    result = mapper.update("UPDATE TOP (2000) t1 SET delete_flag = 1 WHERE delete_flag = 0;");
} while (result > 0);

```

- - - - - -