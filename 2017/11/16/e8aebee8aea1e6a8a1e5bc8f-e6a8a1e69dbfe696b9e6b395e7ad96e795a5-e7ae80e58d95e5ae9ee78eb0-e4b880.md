---
title: '设计模式: 模板方法+策略 简单实现 (一)'
date: '2017-11-16T13:00:00+00:00'
status: publish
permalink: /2017/11/16/%e8%ae%be%e8%ae%a1%e6%a8%a1%e5%bc%8f-%e6%a8%a1%e6%9d%bf%e6%96%b9%e6%b3%95%e7%ad%96%e7%95%a5-%e7%ae%80%e5%8d%95%e5%ae%9e%e7%8e%b0-%e4%b8%80
author: 毛巳煜
excerpt: ''
type: post
id: 235
category:
    - Java
tag: []
post_format: []
hestia_layout_select:
    - default
---
### 开发环境

- 系统: ubuntu 16
- 工具: idea 2017
- jdk: 1.8

### 项目思路

- 每两条数据相比
- 如果被比参数的数据可信度很高, 就设定为不在进行比较
- 将所有维度的可信度加起来为最终这条信息的可信度

### 根据需求分析如下

- 需要两个数据源, 先满足每两条数据相比
- 定义可信度
- 最后统计计算

### 计算公式

- 面积 匹配度计算公式: m = Math.abs(1 - Math.abs(s1 - s2))
- 字符串 匹配度计算公式: m = (匹配的字数 \* 2) / (串1字数 + 串2字数)
- 楼层 匹配度计算公式: m = (f1 == f2) ? 可信度高 : 可信度低;

**计算首先想到的设计模式就是 策略模式, 有了算法就可以面向抽象编程了.**

### 定义策略接口

**用代码来描述大致的功能 或 行为**

```
<pre data-language="">```java
package strategy;

/**
 * 数据去重策略
 * Created by mao-siyu on 17-6-12.
 */
public interface IStrategy {

    /**
     * 算法
     * 计算维度匹配度(m)
     *
     * @param src 源数据
     * @param target 参与匹配的数据
     * @return m 可信度
     */
    float calculation(Object src, Object target);

    /**
     * 使用算法 (java 8 接口新特性之一 default 函数)
     *
     * @param src
     * @param target
     * @return
     */
    default float useStrategy(Object src, Object target) {
        return calculation(src, target);
    }
}

```
```

#### 具体算法实现 实现策略接口

```
<pre data-language="">```java
package strategy.impl;

import strategy.IStrategy;

/**
 * 面积 配度算法
 * Created by mao-siyu on 17-6-12.
 */
public class StrategyAreaImpl implements IStrategy {

    /**
     * @param src
     * @param target
     * @return
     */
    @Override
    public float calculation(Object src, Object target) {
        double s1 = Double.valueOf(src.toString());
        double s2 = Double.valueOf(target.toString());

        // 面积差值不能超过 1
        if (Math.abs(s1 - s2) > 1) {
            return 0;
        } else {
            // 维度匹配度计算公式: m = Math.abs(1 - Math.abs(s1 - s2))
            return (float) Math.abs(1 - Math.abs(s1 - s2));
        }
    }
}

```
```

```
<pre data-language="">```java
package strategy.impl;

import common.RegexEnum;
import strategy.IStrategy;

import java.util.HashSet;
import java.util.Set;

/**
 * 字符 匹配度算法
 * Created by mao-siyu on 17-6-12.
 */
public class StrategyCharacterImpl implements IStrategy {

    @Override
    public float calculation(Object src, Object target) {
        Set<character> srcs = new HashSet();
        Set<character> targets = new HashSet();

        // 将数据解析成集合进行去重
        for (char c : src.toString().replaceAll(RegexEnum.REGEX.toString(), "").toCharArray()) {
            srcs.add(c);
        }
        for (char c : target.toString().replaceAll(RegexEnum.REGEX.toString(), "").toCharArray()) {
            targets.add(c);
        }

        // 匹配的字数
        float matchNum = 0F;
        // 找出去重后的相同数据
        for (Character c : srcs) {
            if (targets.contains(c)) {
                matchNum++;
            }
        }

        // 维度匹配度计算公式: m = (匹配的字数 * 2) / (串1字数 + 串2字数)
        float m = (matchNum * 2) / (srcs.size() + targets.size());

        return m;
    }

}
</character></character>
```
```

```
<pre data-language="">```java
package strategy.impl;


import strategy.IStrategy;

/**
 * 楼层 配度算法
 * Created by mao-siyu on 17-6-12.
 */
public class StrategyFloorImpl implements IStrategy {

    /**
     * @param src
     * @param target
     * @return
     */
    @Override
    public float calculation(Object src, Object target) {
        int f1 = Integer.valueOf(src.toString());
        int f2 = Integer.valueOf(target.toString());

        // 维度匹配度计算公式: m = (f1 == f2) ? 可信度高 : 可信度低;
        float m = (f1 == f2) ? 1F : 0F;
        return m;
    }
}

```
```

**算法类实现完成, 接下来要考虑到不同的数据会有不同的算法, 或者一条数据中也会用到多个算法, 那么接下来还需要一个配置算法该如何使用的类, 配置 初期我想到了 适配器 或者 模板方法, 所以这里我使用了模板方法**

### 模板方法

**先定义这个模板的共同行为**  
\* 让外部调用时, 动态传入数据  
\* 动态获取算法  
\* 应用对应的算法进行比较  
\* 重点: 需要子类提供模板配置

```
<pre data-language="">```java
package template;

import strategy.IStrategy;

import java.util.HashMap;
import java.util.Map;

/**
 * 数据去重 模板
 * Created by mao-siyu on 17-6-12.
 */
public abstract class ABSTemplate {

    // 缓存已经初始化的算法对象
    private Map<string istrategy=""> cache = new HashMap();

    /**
     * 数据比较
     * ====外部调用====
     *
     * @param src    源数据
     * @param target 目标数据
     * @return float
     */
    public float dataCompare(Map<string object=""> src, Map<string object=""> target) {
        return compare(src, target);
    }

    /**
     * 应用对应的算法进行比较
     * ====此方法为灵活考虑, 设置为protected 为子类提供可重写权限====
     *
     * @param src    源数据
     * @param target 目标数据
     * @return m
     */
    protected float compare(Map<string object=""> src, Map<string object=""> target) {

        float tmTotal = 0F;
        float t = 0F;

        for (Map.Entry<string templateinfo=""> entry : getRuleMap().entrySet()) {
            String key = entry.getKey();
            TemplateInfo value = entry.getValue();
            // 公式中的前部分 (t1 * m1 + t2 * m2 .......)
            tmTotal += getStrategy(value.strategy).useStrategy(src.get(key), target.get(key)) * value.t;
            // 公式中的后部分 (t1 + t2 + ......)
            t += value.t;
        }
        // 可信度总合 M = (t1 * m1 + t2 * m2 .......) / (t1 + t2 + ......)
        float M = tmTotal / t;
        return M;
    }

    /**
     * 动态获取算法
     *
     * @param strategyName 策略名称
     * @return IStrategy
     */
    private IStrategy getStrategy(String strategyName) {
        try {

            if (null == cache.get(strategyName)) {
                cache.put(strategyName, (IStrategy) Class.forName("strategy.impl.Strategy" + strategyName + "Impl").newInstance());
            }
        } catch (IllegalAccessException e) {
            e.printStackTrace();
        } catch (InstantiationException e) {
            e.printStackTrace();
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        }
        return cache.get(strategyName);
    }

    /**
     * 此方法 需要子类提供模板配置
     * @return
     */
    protected abstract Map<string templateinfo=""> getRuleMap();

    /**
     * 规范类
     * ====含义为 如果使用这个模板, 至少要符合的要求====
     */
    public static class TemplateInfo {
        // 可信度
        private float t;
        // 策略名
        private String strategy;

        public float getT() {
            return t;
        }

        public void setT(float t) {
            this.t = t;
        }

        public String getStrategy() {
            return strategy;
        }

        public void setStrategy(String strategy) {
            this.strategy = strategy;
        }
    }
}
</string></string></string></string></string></string></string>
```
```

#### 模板实现类

```
<pre data-language="">```java
package template.impl;


import template.ABSTemplate;

import java.util.HashMap;
import java.util.Map;

/**
 * 数据匹配 模板扩展类
 * Created by mao-siyu on 17-6-12.
 */
public class TemplateHouseImpl extends ABSTemplate {

    @Override
    protected Map<string templateinfo=""> getRuleMap() {

        // 定义匹配规则
        Map<string templateinfo=""> mRuleMap = new HashMap();

        TemplateInfo t1 = new TemplateInfo();
        t1.setT(5);
        t1.setStrategy("Character"); // 配置 策略名
        mRuleMap.put("position", t1); // 绑定规则

        t1 = new TemplateInfo();
        t1.setT(9);
        t1.setStrategy("Area"); // 配置 策略名
        mRuleMap.put("area", t1); // 绑定规则

        t1 = new TemplateInfo();
        t1.setT(8);
        t1.setStrategy("Floor"); // 配置 策略名
        mRuleMap.put("floor", t1); // 绑定规则

        return mRuleMap;
    }
}
</string></string>
```
```

### 测试类

```
<pre data-language="">```java
package main;


import template.ABSTemplate;
import template.impl.TemplateHouseImpl;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

/**
 * 测试数据的匹配度
 * Created by mao-siyu on 17-6-13.
 */
public class Test {
    public static void main(String[] args) {

        // 造假数据
        Map<string object=""> src = new HashMap();
        src.put("position", "高新园区 - 大有恬园 - 黄浦路");
        src.put("floor", "12");
        src.put("area", "99.6");
        // 造假数据
        Map<string object=""> target = new HashMap();
//        target.put("position", "高新园区 - 高新园区管委会 - 黄浦路");
//        target.put("floor", "12");
//        target.put("area", "99.6");
        target.put("position", "高新园区 - 大有恬园 - 凌奥街");
        target.put("floor", "12");
        target.put("area", "99");


        int begin = LocalDateTime.now().getNano();
        // 调用模板
        ABSTemplate template = new TemplateHouseImpl();
        // 计算
        float v = template.dataCompare(src, target);
        System.out.println(v);

        System.out.println(LocalDateTime.now().getNano() - begin);
    }
}
</string></string>
```
```

### 枚举类

**为字符串匹配时需要的正则表达式**

```
<pre data-language="">```java
package common;

/**
 * Created by mao-siyu on 17-6-15.
 */
public enum RegexEnum {

    REGEX("[`~!@#$%^&*()+=|{}':;',\\[\\]./?~！@#￥%……&*（）——+|{}【】‘；：”“’。，、？ -]");

    String mResult;

    RegexEnum(String result) {
        this.mResult = result;
    }

    @Override
    public String toString() {
        return mResult;
    }

    public static void main(String[] args) {
//        EnumSet<regexenum> regexEnums = EnumSet.allOf(RegexEnum.class);
//        System.out.println(RegexEnum.CHINESE.toString());
//        regexEnums.stream().forEach((result) -> {
//        });
    }
}
</regexenum>
```
```