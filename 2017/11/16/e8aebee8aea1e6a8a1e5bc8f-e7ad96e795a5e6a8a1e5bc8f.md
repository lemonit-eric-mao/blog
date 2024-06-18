---
title: '设计模式: 策略模式'
date: '2017-11-16T13:01:04+00:00'
status: publish
permalink: /2017/11/16/%e8%ae%be%e8%ae%a1%e6%a8%a1%e5%bc%8f-%e7%ad%96%e7%95%a5%e6%a8%a1%e5%bc%8f
author: 毛巳煜
excerpt: ''
type: post
id: 237
category:
    - Java
tag: []
post_format: []
---
```
<pre class="line-numbers prism-highlight" data-start="1">```java
/**
 * 策略接口,计算购车总金额
 *
 * @author mao_siyu
 */
interface Strategy {
    /**
     * 计算购车总金额
     *
     * @param price 价钱
     * @param num 数量
     * @return
     */
    int calPrice(int price, int num);
}

```
```

**以下是实现不同的算法**

```
<pre class="line-numbers prism-highlight" data-start="1">```java
/**
 * 购买5辆及以下不打折
 *
 * @author mao_siyu
 */
class Nodiscount implements Strategy {

    @Override
    public int calPrice(int price, int num) {

        return price * num;
    }
}

```
```

```
<pre class="line-numbers prism-highlight" data-start="1">```java
/**
 * 购买6-10辆打9.5折
 *
 * @author mao_siyu
 */
class Disount1 implements Strategy {

    @Override
    public int calPrice(int price, int num) {

        return (int) (price * num * 0.95);
    }
}

```
```

```
<pre class="line-numbers prism-highlight" data-start="1">```java
/**
 * 补全,购买11-20辆打9折算法实现
 */
class Disount2 implements Strategy {

    @Override
    public int calPrice(int price, int num) {

        return (int) (price * num * 0.9);
    }
}

```
```

```
<pre class="line-numbers prism-highlight" data-start="1">```java
/**
 * 补全,购买20辆以上打8.5折算法实现
 *
 * @author mao_siyu
 */
class Disount3 implements Strategy {

    @Override
    public int calPrice(int price, int num) {

        return (int) (price * num * 0.85);
    }
}

```
```

### 这个类是用来生成不同的策略对象的

```
<pre class="line-numbers prism-highlight" data-start="1">```java
/**
 * 上下文,根据不同策略来计算购车总金额
 *
 * @author mao_siyu
 */
class Context {

    private Strategy strategy;

    public Context(Strategy strategy) {
        this.strategy = strategy;
    }

    public int calPrice(int price, int num) {

        // 补全,计算价格算法
        return strategy.calPrice(price, num);
    }
}

```
```

### 测试

```
<pre class="line-numbers prism-highlight" data-start="1">```java
public class Main {

    /*
     * 每辆车单价10000
     */
    public static void main(String[] args) {

        Strategy strategy;
        // 计算购买3辆总金额
        strategy = new Nodiscount();
        Context context = new Context(strategy);
        System.out.println("购买3辆总金额: " + context.calPrice(10000, 3));
        // 补全 计算12辆总金额
        strategy = new Disount2();
        context = new Context(strategy);
        System.out.println("购买12辆总金额: " + context.calPrice(10000, 12));
    }

}

```
```