---
title: 'Java 枚举 做计算器'
date: '2017-11-16T13:09:39+00:00'
status: publish
permalink: /2017/11/16/java-%e6%9e%9a%e4%b8%be-%e5%81%9a%e8%ae%a1%e7%ae%97%e5%99%a8
author: 毛巳煜
excerpt: ''
type: post
id: 261
category:
    - Java
tag: []
post_format: []
---
```
<pre class="line-numbers prism-highlight" data-start="1">```java
package myMain;

public enum Menum {

    ADD {

        public String calc(double a, double b) {

            return String.valueOf(a + b);
        }

    },

    SUB {

        @Override
        public String calc(double a, double b) {

            return String.valueOf(a - b);
        }

    },
    MUL {

        @Override
        public String calc(double a, double b) {

            return String.valueOf(a * b);
        }
    },
    DIV {

        @Override
        public String calc(double a, double b) {

            return String.valueOf(a / b + a % b);
        }
    };

    public abstract String calc(double a, double b);

    public static void main(String[] args) {

        mCalc(Menum.MUL, 4, 2);
    }

    public static void mCalc(Menum m, double a, double b) {

        String result = m.calc(a, b);
        System.out.println(result);
    }
}

```
```