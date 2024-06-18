---
title: 'Hadoop 2.x 理论学习笔记'
date: '2017-11-16T15:15:29+00:00'
status: publish
permalink: /2017/11/16/hadoop-2-x-%e7%90%86%e8%ae%ba%e5%ad%a6%e4%b9%a0%e7%ac%94%e8%ae%b0
author: 毛巳煜
excerpt: ''
type: post
id: 482
category:
    - 大数据
tag: []
post_format: []
hestia_layout_select:
    - default
---
### Hadoop 2.x

`Hadoop 2.0 以后的版本移除了原有的JobTracker和TaskTracker, 改由Yan平台的ResourceManager负责集群中所有资源的统一管理和分配, NodeManager管理Hadoop集群中单个计算节点.`

```
<pre class="line-numbers prism-highlight" data-start="1">```ruby
[root@sp-64 ~]# jps
7809 NameNode
7083 NodeManager
6969 ResourceManager
6626 DataNode
6803 SecondaryNameNode
19138 Jps
[root@sp-64 ~]#

```
```

### MapReduce 作业流程

`MapReduce作业是一种大规模数据集的并行计算的编程模型. 我们可以将HDFS中存放的海量数据, 通过MapReduce作业进行计算, 得到目标数据! 它的作业流程分为四个阶段:`

- **(1) Split 阶段**  
  `Split阶段 也叫做分片输入阶段. 例如: 下面有三行文本`  
  **Hello, i love coding  
  are you ok?  
  Hello, i love hadoop**  
  `经过分片处理之后产生了三个分片每一个分片就是一行文本`  
  **输出**  
  `Hello, i love coding`  
  `are you ok?`  
  `Hello, i love hadoop`

`这个阶段的输出作为 Map阶段 的输入`

- - - - - -

- **(2) Map 阶段(需要自己写逻辑)**

**输入<key value=""></key>**

```
<pre class="line-numbers prism-highlight" data-start="1">```null




```
```

`经过Map拆分后的数据格式`

**输出<key value=""></key>**

```
<pre class="line-numbers prism-highlight" data-start="1">```null
<hello>
<i>
<love>
<coding>

<are>
<you>
<ok>

<hello>
<i>
<love>
<hadoop>
</hadoop></love></i></hello></ok></you></are></coding></love></i></hello>
```
```

`这个阶段的输出作为 Shuffle阶段 的输入`

- - - - - -

- **(3) Shuffle(混洗) 阶段**  
  `Shuffle阶段 过程比较复杂, 可以理解为从Map输出到Reduce输入的过程, 而且涉及到网络传输.这个过程就是将上面的单词规整到一起, 但并不做次数的累加!`

**输出**

```
<pre class="line-numbers prism-highlight" data-start="1">```null
<hello>
<i>
<love>
<coding>
<are>
<you>
<ok>
<hadoop>
</hadoop></ok></you></are></coding></love></i></hello>
```
```

`这个阶段的输出作为 Reduce阶段 的输入`

- - - - - -

- **(4) Reduce 阶段(需要自己写逻辑)**  
  `Reduce阶段 会对单词出现的次数进行累加求和, 当所有的计算全部完成, 最终输出所有结果.`

**输入<key value=""></key>**

```
<pre class="line-numbers prism-highlight" data-start="1">```null
<hello>
<i>
<love>
<coding>
<are>
<you>
<ok>
<hadoop>
</hadoop></ok></you></are></coding></love></i></hello>
```
```

**输出<key value=""></key>**

```
<pre class="line-numbers prism-highlight" data-start="1">```null
<hello>
<i>
<love>
<coding>
<are>
<you>
<ok>
<hadoop>
</hadoop></ok></you></are></coding></love></i></hello>
```
```

### 最终输出的结果是

```
<pre class="line-numbers prism-highlight" data-start="1">```null
Hello  2
i      2
love   2
coding 1
are    1
you    1
ok?    1
hadoop 1

```
```

- - - - - -

- - - - - -

- - - - - -

### 一个MapReduce作业中, 以下三者的数量总是相等的

```
<pre class="line-numbers prism-highlight" data-start="1">```null
一个MapReduce作业中
(1)Partitioner的数量
(2)Reduce任务的数量
(3)最终输出的文件的数量(如:part-r-00000)
它们的数量总是相等的;
并且在一个Reducer中, 所有的数据都会被按照key值升序排序, 故如果part输出文件中包含key值, 那么这个文件一定是有序的.

```
```

### Reduce 任务数量

`在大数据量的情况下, 如果只设置1个Reduce任务, 那么在Reduce阶段, 整个集群只有该节点在运行Reduce任务,其它节点都将被闲置, 效率十分低下. 故建议将Reduce任务数量设置成一个较大的值(最大值是72).`

### 本地合并 Combine

`Combine: 数据在Mapper输出后会进行和Reducer相似的操作, 减少网络开销. 通过job.setCombinerClass(MyReduce.class);这行代码就可以设置这些操作`

- - - - - -

### 总结 Mapper-Shuffle-Reducer

- **Combine本质上是在Mapper缓冲区溢写文件的合并, 目地是减少网络开销.**
- **Partition是在Reduce输入之前发生, 相同的key值一定会进入同一个Partitioner, 并且在Reduce过程默认会按照key值升序排序.**
- **Partitioner、Reducer、输出文件，三者数量是相等的.**
- **大数据量的情况下，Reducer数量不宜过少，可以通过两种方式设置：  
  （1）在代码中设置job.setNumReduceTasks(int n)  
  （2）在配置文件中设置 mapred.reduce.tasks  
  两种方式选一种即可**