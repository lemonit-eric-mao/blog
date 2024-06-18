---
title: java枚举简单应用
date: '2017-11-16T12:58:01+00:00'
status: publish
permalink: /2017/11/16/java%e6%9e%9a%e4%b8%be%e7%ae%80%e5%8d%95%e5%ba%94%e7%94%a8
author: 毛巳煜
excerpt: ''
type: post
id: 233
category:
    - Java
tag: []
post_format: []
---
```
<pre class="line-numbers prism-highlight" data-start="1">```java
package com.housecenter.dlfc.framework.cleandata.common.util;

import java.util.EnumSet;

/**
 * Created by mao-siyu on 17-6-15.
 */
public enum RegexEnum {

    REGEX("[`~!@#$%^&*()+=|{}':;',\\[\\]./?~！@#￥%……&*（）——+|{}【】‘；：”“’。，、？ -]"),
    CHINESE("[^\\x00-\\xff]"),
    ENGLISH("[a-zA-Z]"),
    NOTENGLISH("[^a-z^A-Z]"),
    NUMBER("[0-9]"),
    NOTNUMBER("[^0-9]");

    String mResult;

    RegexEnum(String result) {
        this.mResult = result;
    }

    public String toString() {
        return mResult;
    }

//    public static void main(String[] args) {
//        EnumSet<regexenum> regexEnums = EnumSet.allOf(RegexEnum.class);
//        regexEnums.stream().forEach((result) -> {
//            System.out.println(result);
//        });
//    }
}
</regexenum>
```
```