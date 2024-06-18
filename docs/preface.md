# 前言

### 用更少的代码，更短的编译时间，创建运行更快的程序，享受更多的乐趣	

对于学习 Go 编程语言的爱好者来说，这本书无疑是最适合你的一本书籍，这里包含了当前最全面的学习资源。本书通过对官方的在线文档、名人博客、书籍、相关文章以及演讲的资料收集和整理，并结合我自身在软件工程、编程语言和数据库开发的授课经验，将这些零碎的知识点组织成系统化的概念和技术分类来进行讲解。

随着软件规模的不断扩大，诸多的学者和谷歌的开发者们在公司内部的软件开发过程中开始经历大量的挫折，在诸多问题上都不能给出令人满意的解决方案，尤其是在使用 C++ 来开发大型的服务端软件时，情况更是不容乐观。由于二进制文件一般都是非常巨大的，因此需要耗费大量的时间在编译这些文件上，同时编程语言的设计思想也已经非常陈旧，这些情况都充分证明了现有的编程语言已不符合时下的生产环境。尽管硬件在过去的几十年中有了飞速的发展，但人们依旧没有找到机会去改变 C++ 在软件开发的重要地位，并在实际开发过程中忍受着它所带来的令人头疼的一些问题。因此学者们坐下来总结出了现在生产环境与软件开发之间的主要矛盾，并尝试设计一门全新的编程语言来解决这些问题。

以下就是他们讨论得出的对编程语言的设计要求：

- 能够以更快的速度开发软件
- 开发出的软件能够很好地在现代的多核计算机上工作
- 开发出的软件能够很好地在网络环境下工作
- 使人们能够享受软件开发的过程

Go 语言就在这样的环境下诞生了，它让人感觉像是 Python 或 Ruby 这样的动态语言，但却又拥有像 C 或者 Java 这类语言的高性能和安全性。

``` go
type KubeConfig struct {
}
```

``` yaml
apiVersion: v1
kind: Service
metadata:
  name: nginx-svc
spec:
  ports:
  - name: web
    port: 80
    protocol: TCP
    targetPort: 80
  selector:
    app: nginx
  type: ClusterIP
```