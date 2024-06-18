---
title: 'Java 8 Lambda.stream()'
date: '2019-12-18T05:48:07+00:00'
status: publish
permalink: /2019/12/18/java-8-lambda-stream
author: 毛巳煜
excerpt: ''
type: post
id: 5197
category:
    - Java
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### 1 list 转 map

```java
class Test {

    private String id;

    private String name;

    public Test(String id, String name) {
        this.id = id;
        this.name = name;
    }

    public String getId() {
        return id;
    }

    public static void main(String[] args) {

        List<test> ts = new ArrayList();
        ts.add(new Test("001", "张三"));
        ts.add(new Test("002", "李四"));
        ts.add(new Test("003", "田七"));
        ts.add(new Test("004", "赵四"));

        Map<string test=""> map = ts.stream().collect(Collectors.toMap(Test::getId, Function.identity()));

        System.out.println(map);

    }
}
</string></test>
```