---
title: 面向对象设计原则-OOD
date: '2017-11-16T13:01:29+00:00'
status: publish
permalink: /2017/11/16/%e8%ae%be%e8%ae%a1%e6%a8%a1%e5%bc%8f-%e5%8e%9f%e5%88%99
author: 毛巳煜
excerpt: ''
type: post
id: 239
category:
    - Java
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
[OOD 原则](http://butunclebob.com/ArticleS.UncleBob.PrinciplesOfOod)

- - - - - -

> - **前五项是`设计原则`**  
>   <table><thead><tr><th align="left">英文</th><th align="center">缩写</th><th align="left">中文</th><th align="left">概念</th><th align="left">备注</th></tr></thead><tbody><tr><td align="left">Single Responsibility Principle</td><td align="center">SRP</td><td align="left">单一职责原则</td><td align="left">改变一个类应该只有一个理由</td><td align="left"></td></tr><tr><td align="left">Open Closed Principle</td><td align="center">OCP</td><td align="left">开闭原则</td><td align="left">您应该能够扩展类行为，而无需修改它</td><td align="left">对扩展开放，对修改关闭</td></tr><tr><td align="left">Liskov Substitution Principle</td><td align="center">LSP</td><td align="left">里氏替换原则</td><td align="left">派生类必须可替换为其基类</td><td align="left">子类必须能够替换掉它们的父类</td></tr><tr><td align="left">Interface Segregation Principle</td><td align="center">ISP</td><td align="left">接口隔离原则</td><td align="left">客户端不应该被强迫实现一些他们不会使用的接口</td><td align="left">就是使用多个专门的接口比使用单个接口要好很多</td></tr><tr><td align="left">Dependency Inversion Principle</td><td align="center">DIP</td><td align="left">依赖倒置原则</td><td align="left">依赖于抽象，而不是实体</td><td align="left">程序要依赖于抽象接口，不要依赖于具体实现。</td></tr></tbody></table>

- - - - - -

> - **接下来的六条原则是`关于软件包`的**。在这种情况下，**`包`是一个`二进制可交付文件`**，如**.jar** 文件或 **dll**，而不是一个名称空间，如java包或C++名称空间。
> - **前三个包原则是关于`包内聚性`的，它们告诉我们在包中放什么**  
>   <table><thead><tr><th align="left">英文</th><th align="center">缩写</th><th align="left">中文</th><th align="left">概念</th><th align="left">备注</th></tr></thead><tbody><tr><td align="left">Release Reuse Equivalency Principle</td><td align="center">REP</td><td align="left">复用/发布等同原则</td><td align="left">重用的颗粒就是发布的颗粒</td><td align="left">软件复用的最小粒度应等同于其发布的最小粒度，需要有自己的发布版本号</td></tr><tr><td align="left">Common Closure Principle</td><td align="center">CCP</td><td align="left">共同闭包原则</td><td align="left">将一起更改的类打包在一起</td><td align="left">在包中，包含的所有类应该是对同类的变化的一个集合，也就是说，如果对包做出修改，需要调整的类应该都在这个包之内</td></tr><tr><td align="left">Common Reuse Principle</td><td align="center">CRP</td><td align="left">共同复用原则</td><td align="left">将一起使用的类打包在一起</td><td align="left">不要强迫一个组件的用户依赖他们不需要的东西。建议我们将经常共同复用的类和模块放在同一个组件中</td></tr></tbody></table>

- - - - - -

> - **最后三条原则是关于`包之间的耦合`，并讨论评估系统包结构的指标**  
>   <table><thead><tr><th align="left">英文</th><th align="center">缩写</th><th align="left">中文</th><th align="left">概念</th><th align="left">备注</th></tr></thead><tbody><tr><td align="left">Acyclic Dependencies Principle</td><td align="center">ADP</td><td align="left">非循环依赖原则</td><td align="left">包的依赖必须没有循环</td><td align="left">包之间的依赖关系不可以形成循环</td></tr><tr><td align="left">Stable Dependencies Principle</td><td align="center">SDP</td><td align="left">稳定依赖性原则</td><td align="left">依赖于稳定的方向</td><td align="left">**`稳定依赖性`**即满足以下条件：  
>   1. 开发已经完成  
>   2. 运行环境确定或者对运行环境的变动不敏感，例如：只在某些机器某些版本的系统上运行。  
>   3. 有着可预期的行为模式，例如：此模块只做xxx功能。  
>   4. 持续性长，后期几乎无改动   
>   5. 其对外无依赖或者依赖项也属于稳定性依赖且数量少</td></tr><tr><td align="left">Stable Abstractions Principle</td><td align="center">SAP</td><td align="left">稳定抽象原则</td><td align="left">抽象性随稳定性而增加</td><td align="left">一个组件的抽象化程度应该与其稳定性保持一致</td></tr></tbody></table>

- - - - - -