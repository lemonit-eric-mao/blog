---
title: "Java 枚举 做计算器"
date: "2017-11-16"
categories: 
  - "java"
---

```java
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
