---
title: "java枚举简单应用"
date: "2017-11-16"
categories: 
  - "java"
---

```java
package com.housecenter.dlfc.framework.cleandata.common.util;

import java.util.EnumSet;

/**
 * Created by mao-siyu on 17-6-15.
 */
public enum RegexEnum {

    REGEX("[`~!@#$%^&amp;*()+=|{}':;',\\[\\].<>/?~！@#￥%……&amp;*（）——+|{}【】‘；：”“’。，、？ -]"),
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
//        EnumSet<RegexEnum> regexEnums = EnumSet.allOf(RegexEnum.class);
//        regexEnums.stream().forEach((result) -> {
//            System.out.println(result);
//        });
//    }
}
```
