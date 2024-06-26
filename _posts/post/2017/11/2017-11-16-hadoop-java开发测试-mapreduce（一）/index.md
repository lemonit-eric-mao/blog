---
title: "Hadoop Java开发测试 MapReduce（一）"
date: "2017-11-16"
categories: 
  - "大数据"
---

- 开发工具: IDEA
- 应用系统: ubuntu 10.04
- 项目类型: maven
- 工程名称: MyHadoop
- 项目路径: ![](images/project_path.png)

### **pom.xml**

```markup
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>blog.com</groupId>
    <artifactId>blog</artifactId>
    <version>1.0-SNAPSHOT</version>

    <dependencies>
        <!-- https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-common -->
        <dependency>
            <groupId>org.apache.hadoop</groupId>
            <artifactId>hadoop-common</artifactId>
            <version>2.8.1</version>
        </dependency>
        <!-- https://mvnrepository.com/artifact/org.apache.hadoop/hadoop-mapreduce-client-core -->
        <dependency>
            <groupId>org.apache.hadoop</groupId>
            <artifactId>hadoop-mapreduce-client-core</artifactId>
            <version>2.8.1</version>
        </dependency>

    </dependencies>

    <!-- maven build插件, 打jar包时指定jar包入口 -->
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-shade-plugin</artifactId>
                <version>1.2.1</version>
                <executions>
                    <execution>
                        <phase>package</phase>
                        <goals>
                            <goal>shade</goal>
                        </goals>
                        <configuration>
                            <transformers>
                                <transformer implementation="org.apache.maven.plugins.shade.resource.ManifestResourceTransformer">
                                    <mainClass>WordMain</mainClass>
                                </transformer>
                            </transformers>
                        </configuration>
                    </execution>
                </executions>
            </plugin>
        </plugins>
    </build>
</project>
```

### **WordMapper.java**

```java
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

import java.io.IOException;
import java.util.StringTokenizer;

/**
 * MapReduce中的Map扩展类
 * 
 * Mapper
 *
 * @author mao-siyu
 */
public class WordMapper extends Mapper {

    /**
     * 输出的Value
     */
    private static final IntWritable one = new IntWritable(1);

    /**
     * 输出的Key
     */
    private Text word = new Text();

    /**
     * 文件中的每读取到一行数据 就会执行一次这个函数
     *
     * @param key
     * @param value
     * @param context
     * @throws IOException
     * @throws InterruptedException
     */
    @Override
    protected void map(Object key, Text value, Context context) throws IOException, InterruptedException {
        StringTokenizer stringTokenizer = new StringTokenizer(value.toString());
        while (stringTokenizer.hasMoreTokens()) {
            word.set(stringTokenizer.nextToken());
            // 将Mapper的输出数据传给Reduce做为它的的输入数据
            context.write(word, one);
        }
    }
}
```

### **WordReduce.java**

```java
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

import java.io.IOException;

/**
 * MapReduce中的Reduce扩展类
 * 
 * Reducer
 *
 * @author mao-siyu
 */
public class WordReduce extends Reducer {

    /**
     * 输出的Value
     */
    private IntWritable result = new IntWritable();

    @Override
    protected void reduce(Text key, Iterable values, Context context) throws IOException, InterruptedException {

        int sum = 0;
        for (IntWritable value : values) {
            sum += value.get();
        }
        result.set(sum);
        // Reduce 输出数据
        context.write(key, result);
    }
}
```

### **WordMain.java**

```java
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

/**
 * Created by mao-siyu on 17-9-5.
 */
public class WordMain {
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        List list = new ArrayList(Arrays.asList(new GenericOptionsParser(conf, args).getRemainingArgs()));

        if (list.size() != 2) {

            System.out.println("otherArgs.length    =:|======>    " + list.size());
            System.err.println("Usage    =:|======>    wordcount  ");
            for (String str : list) {
                System.out.println("=:|======>    " + str);
            }
//            System.exit(2);
            list.remove(0);
        }

        Job job = Job.getInstance(conf, "word count");
        job.setJarByClass(WordMain.class); // 主类
        job.setMapperClass(WordMapper.class); // Mapper
        job.setCombinerClass(WordReduce.class); // 作业合成类
        job.setReducerClass(WordReduce.class); // Reducer
        job.setOutputKeyClass(Text.class); // 设置作业输出数据的关键类
        job.setOutputValueClass(IntWritable.class); // 设置作业输出值类

        FileInputFormat.addInputPath(job, new Path(list.get(0))); // 文件输入
        FileOutputFormat.setOutputPath(job, new Path(list.get(1))); // 文件输出

        System.exit(job.waitForCompletion(true) ? 0 : 1); // 等待完成退出
    }
}
```

### **IDEA 使用maven 打jar包**

![](images/maven_package.png)

### **最后将jar包 发送到 master 服务器的 /home/myhadoop/hadoop-2.8.1/**

`blog-1.0-SNAPSHOT.jar`

```ruby
mao-siyu@mao-siyu-PC:~/IDEAProjects/MyHadoop/target$ scp blog-1.0-SNAPSHOT.jar root@10.32.156.64:/home/myhadoop/hadoop-2.8.1
root@10.32.156.64's password:
blog-1.0-SNAPSHOT.jar                         100%   29MB  28.8MB/s   00:00
mao-siyu@mao-siyu-PC:~/IDEAProjects/MyHadoop/target$
```

# **测试 MapReduce**

### **删除之前测试的文件/文件夹**

`hadoop fs -rm -r -f 删除文件夹及文件`

```ruby
[root@sp-64 ~]# hadoop fs -rm /user/hadoop/input/test.txt
[root@sp-64 hadoop-2.8.1]# hadoop fs -rm -r -f /user/hadoop/output/
Deleted /user/hadoop/output
[root@sp-64 hadoop-2.8.1]#
```

#### **file1.txt 内容**

```ruby
Hello, i love coding
are you ok?
Hello, i love hadoop
are you ok?
```

#### **file2.txt 内容**

```ruby
Hello i love coding
are you ok ?
Hello i love hadoop
are you ok ?
```

### **上传 file1.txt file2.txt 文件到 HDFS 系统的input文件夹下**

```ruby
[root@sp-64 ~]# ll
总用量 8
-rw-r--r-- 1 root root 68 9月   5 15:24 file1.txt
-rw-r--r-- 1 root root 68 9月   5 15:24 file2.txt
[root@sp-64 ~]#
[root@sp-64 ~]# hadoop fs -put file1.txt /user/hadoop/input/
[root@sp-64 ~]# hadoop fs -put file2.txt /user/hadoop/input/
```

### **查看上传文件是否成功**

```ruby
[root@sp-64 ~]# hadoop fs -ls /user/hadoop/input/
Found 2 items
-rw-r--r-- 1 root supergroup         68 2017-09-05 15:25 /user/hadoop/input/file1.txt
-rw-r--r-- 1 root supergroup         68 2017-09-05 15:25 /user/hadoop/input/file2.txt
[root@sp-64 ~]#
```

### **测试**

```ruby
[root@sp-64 hadoop-2.8.1]# hadoop jar blog-1.0-SNAPSHOT.jar WordMain /user/hadoop/input/file* /user/hadoop/output
otherArgs.length    =:|======>    3
Usage    =:|======>    wordcount  
=:|======>    WordMain
=:|======>    /user/hadoop/input/file*
=:|======>    /user/hadoop/output
# 以下的输出信息在这里省略
```

### **查看测试结果**

```ruby
[root@sp-64 hadoop-2.8.1]#
[root@sp-64 hadoop-2.8.1]# hadoop fs -ls /user/hadoop/output/
Found 2 items
-rw-r--r-- 1 root supergroup          0 2017-09-05 16:29 /user/hadoop/output/_SUCCESS
-rw-r--r-- 1 root supergroup         73 2017-09-05 16:29 /user/hadoop/output/part-r-00000
[root@sp-64 hadoop-2.8.1]# hadoop fs -text /user/hadoop/output/part-r-00000
?   2
Hello   2
Hello,  2
are 4
coding  2
hadoop  2
i   4
love    4
ok  2
ok? 2
you 4
[root@sp-64 hadoop-2.8.1]#
```
