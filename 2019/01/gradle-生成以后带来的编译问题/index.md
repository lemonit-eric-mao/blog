---
title: "gradle 生级4.6以后带来的编译问题"
date: "2019-01-31"
categories: 
  - "移动端"
---

##### implementation 与 api 两种引用方式的区别

```json
dependencies {
    // 使用 implementation 引入的jar包 只能被自己使用
    implementation fileTree(include: ['*.jar'], dir: 'libs')
    // 使用 api 引入的jar包，当自己被其它项目引用的时候，自己引入的jar包也可以被使用 相当于 public
    api files('libs/FaceSDK_2.0.0.1.jar')
}
```

##### 拿百度人脸识别官方的Demo举例：

###### 两个项目:

1. facesample 项目
2. facelibrary 项目

###### facesample项目的部分 build.gradle

```json
dependencies {
    implementation fileTree(include: ['*.jar'], dir: 'libs')
    implementation 'com.android.support:appcompat-v7:28.0.0'
    // 引用 facelibrary 项目
    implementation project(':facelibrary')
}
```

###### facelibrary 项目的部分 build.gradle

```json
dependencies {
    implementation fileTree(include: ['*.jar'], dir: 'libs')
    // 这种引用方式 facesample 项目是可以引用 FaceSDK.jar 的
    api files('libs/FaceSDK_2.0.0.1.jar')
    // 这种引用方式 facesample 项目是无法引用的
    implementation files('libs/FaceSDK_2.0.0.1.jar')
}
```
