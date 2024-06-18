---
title: "Java 8 Lambda.stream()"
date: "2019-12-18"
categories: 
  - "java"
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

        List<Test> ts = new ArrayList<>();
        ts.add(new Test("001", "张三"));
        ts.add(new Test("002", "李四"));
        ts.add(new Test("003", "田七"));
        ts.add(new Test("004", "赵四"));

        Map<String, Test> map = ts.stream().collect(Collectors.toMap(Test::getId, Function.identity()));

        System.out.println(map);

    }
}
```
