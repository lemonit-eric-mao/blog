---
title: 'Go 语言学习笔记'
date: '2022-03-16T05:30:58+00:00'
status: publish
permalink: /2022/03/16/go-%e8%af%ad%e8%a8%80%e5%ad%a6%e4%b9%a0%e7%ac%94%e8%ae%b0
author: 毛巳煜
excerpt: ''
type: post
id: 8399
category:
    - Go
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
##### Go 程序的执行（程序启动）顺序如下：

1. 按顺序导入所有被 main 包引用的其它包，然后在每个包中执行如下流程：
2. 如果该包又导入了其它的包，则从第一步开始递归执行，但是每个包只会被导入一次。
3. 然后以相反的顺序在每个包中初始化常量和变量，如果该包含有 init 函数的话，则调用该函数。
4. 在完成这一切之后，main 也执行同样的过程，最后调用 main 函数开始执行程序。

- - - - - -

- - - - - -

- - - - - -

##### **[注意事项](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/16.0.md#160-%E5%B8%B8%E8%A7%81%E7%9A%84%E9%99%B7%E9%98%B1%E4%B8%8E%E9%94%99%E8%AF%AF "注意事项")**

1. 如果你导入了一个包却没有使用它，则会在构建程序时引发错误，如 **`imported and not used: os`** 这正是遵循了 Go 的格言： **`没有不必要的代码！`** 。
2. **Go 是`强类型`语言** ，因此不会进行隐式转换，任何不同类型之间的转换都必须显式说明。 Go 不存在像 C 那样的运算符重载，表达式的解析顺序是从左至右
3. 当一个函数在其函数体内调用自身，则称之为**递归**。最经典的例子便是计算**斐波那契数列**，即前两个数为1，从第三个数开始每个数均为前两个数之和。  
  在使用递归函数时经常会遇到的一个重要问题就是栈溢出：一般出现在大量的递归调用导致的程序栈内存分配耗尽。这个问题可以通过一个名为**[惰性求值](https://zh.wikipedia.org/wiki/%E6%83%B0%E6%80%A7%E6%B1%82%E5%80%BC "惰性求值")** 的技术解决。  
  在 Go 语言中，我们可以使用 **管道（channel）** 和 **协程（goroutine）** 来实现，通过 **[链式协程](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/14.12.md#1412-%E9%93%BE%E5%BC%8F%E5%8D%8F%E7%A8%8B "链式协程")** 这个方案来**优化斐波那契数列**的生成问题。

4. **不需要将一个指向切片的`指针`传递给函数**
  - 当**切片**作为**参数传递**时，切记**不要解引用**切片。

5. **使用`指针`指向接口类型**
  - **永远不要使用**一个**指针指向**一个**接口**类型，因为它 **`已经是一个指针`** 。

6. **使用值类型时误用`指针`**
  - 将一个**值类型**作为一个**参数传递**给函数或者作为一个方法的接收者，似乎**是对内存的滥用**，因为**值类型一直是传递拷贝**。
  - 但是另一方面，**值类型的内存是在`栈`上分配**，内存分配快速且开销不大。**如果你`传递一个指针`**，而不是一个值类型，**Go编译器**大多数情况下**会认为需要创建一个对象**，**并将对象移动到堆上**，所以会导致**额外的内存分配**; 因此当使用指针代替值类型作为参数传递时，我们没有任何收获。

7. **`误用`协程和通道**
  - 当且仅当**代码中并发执行非常重要时**，才使用协程和通道。

8. **[Go 同时支持面向过程和面向对象编程](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/17.4.md#174-%E8%BF%90%E7%AE%97%E7%AC%A6%E6%A8%A1%E5%BC%8F%E5%92%8C%E6%8E%A5%E5%8F%A3 "Go 同时支持面向过程和面向对象编程")**
9. **[出于性能考虑的最佳实践和建议](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/18.11.md#1811-%E5%87%BA%E4%BA%8E%E6%80%A7%E8%83%BD%E8%80%83%E8%99%91%E7%9A%84%E6%9C%80%E4%BD%B3%E5%AE%9E%E8%B7%B5%E5%92%8C%E5%BB%BA%E8%AE%AE "出于性能考虑的最佳实践和建议")**  
  （1）尽可能的使用 `:=` 去初始化声明一个变量（在函数内部）；  
  （2）尽可能的使用`字符`代替`字符串`；  
  （3）尽可能的使用`切片`代替`数组`；  
  （4）尽可能的使用`数组和切片`代替`映射`；  
  （5）如果只想获取切片中某项值，不需要值的索引，尽可能的使用 `for range` 去遍历切片，这比必须查询切片中的每个元素要快一些；  
  （6）当数组元素是稀疏的（例如有很多 0 值或者空值 nil），使用映射会降低内存消耗；  
  （7）初始化映射时指定其容量；  
  （8）当定义一个方法时，使用指针类型作为方法的接受者；  
  （9）在代码中使用常量或者标志提取常量的值；  
  （10）尽可能在需要分配大量内存时使用缓存；  
  （11）使用缓存模板

- 永远不要使用形如`var p*a` 声明变量，这会混淆指针声明和乘法运算（参考4.9小节）
- 永远不要在 `for` 循环自身中改变计数器变量（参考5.4小节）
- 永远不要在 `for-range` 循环中使用一个值去改变自身的值（参考5.4.4小节）
- 永远不要将 `goto` 和前置标签一起使用（参考5.6小节）
- 永远不要忘记在函数名（参考第6章）后加括号()，尤其调用一个对象的方法或者使用匿名函数启动一个协程时
- 永远不要使用 `new() 一个 map`，一直使用 `make`（参考第8章）
- 当为一个类型定义一个 `String()` 方法时，不要使用 `fmt.Print` 或者类似的代码（参考10.7小节）
- 永远不要忘记当终止缓存写入时，使用 `Flush` 函数（参考12.2.3小节）
- 永远不要忽略错误提示，忽略错误会导致程序崩溃（参考13.1小节）
- 不要使用全局变量或者共享内存，这会使并发执行的代码变得不安全（参考14.1小节）
- `println` 函数仅仅是用于调试的目的

**最佳实践：对比以下使用方式：**

- 使用正确的方式初始化一个元素是切片的映射，例如 `map[type]slice`（参考8.1.3小节）
- 一直使用逗号`，ok` 或者 `checked` 形式作为类型断言（参考11.3小节）
- 使用一个工厂函数创建并初始化自己定义类型（参考10.2小节-18.4小节）
- 仅当一个结构体的方法想改变结构体时，使用结构体指针作为方法的接受者，否则使用一个结构体值类型10.6.3小节

- - - - - -

- - - - - -

- - - - - -

##### **`rune`** 是什么类型？

 其实 rune 也是 Go 当中的一个类型，并且是 int32 的别名。**[详见官方文档](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/04.5.md#455-%E5%AD%97%E7%AC%A6%E7%B1%BB%E5%9E%8B "详见官方文档")**

- - - - - -

- - - - - -

- - - - - -

##### **`Itoa`、`Atoi`**是什么意思？

 `strconv.Itoa(i int) string` 返回数字 i 所表示的字符串类型的十进制数。  
 `strconv.Atoi(s string) (i int, err error)` 将字符串转换为 int 型

 刚接触Go语言时对 **Itoa()、Atoi()** 函数比较懵，为了方便理解，改为如下形式：

- **a 表示 string**
  - Itoa() **int to string**
  - Atoi() **string to int**

**[详见官方文档](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/04.7.md#4712-%E5%AD%97%E7%AC%A6%E4%B8%B2%E4%B8%8E%E5%85%B6%E5%AE%83%E7%B1%BB%E5%9E%8B%E7%9A%84%E8%BD%AC%E6%8D%A2 "详见官方文档")**

- - - - - -

- - - - - -

- - - - - -

##### 特殊的标识符，下划线 **`_`**

 **`_`** 本身就是一个特殊的标识符，被称为空白标识符。它可以像其他标识符那样用于变量的声明或赋值（任何类型都可以赋值给它）， **但任何赋给这个标识符的值`都将被抛弃`** ，因此这些值不能在后续的代码中使用，也不可以使用这个标识符作为变量对其它变量进行赋值或运算。  
 **`_`** 实际上是一个只写变量，你不能得到它的值。这样做是因为 Go 语言中你必须使用所有被声明的变量，但有时你并不需要使用从一个函数得到的所有返回值。

- - - - - -

- - - - - -

- - - - - -

##### if{} else if{} else{}

 if 可以包含一个初始化语句（如：给一个变量赋值）。这种写法具有固定的格式（在初始化语句后方必须加上分号）  
 但要注意的是，使用简短方式 **`:=`** 声明的变量的作用域只存在于 if 结构中（在 if 结构的大括号之间，如果使用 if-else 结构则在 else 代码块中变量也会存在）。  
[![](http://qiniu.dev-share.top/image/png/Go_if_else.png)](http://qiniu.dev-share.top/image/png/Go_if_else.png)

 如果变量在 if 结构之前就已经存在，那么在 if 结构中，该变量原来的值会被隐藏。

```go
package main

import (
    "fmt"
)

func main() {

    temp := "def"

    if temp := "abc"; true {
        fmt.Println(temp)      // abc
    } else if !true {
        fmt.Println(temp)      // abc
    } else {
        fmt.Println(temp)      // abc
    }

    fmt.Println(temp)          // def

}


```

- - - - - -

- - - - - -

- - - - - -

##### 内置函数

<table><thead><tr><th align="left">名称</th><th align="left">说明</th></tr></thead><tbody><tr><td align="left">close</td><td align="left">用于管道通信</td></tr><tr><td align="left">len、cap</td><td align="left">len 用于返回某个类型的长度或数量（字符串、数组、切片、map 和管道）；  
cap 是容量的意思，用于返回某个类型的最大容量（只能用于数组、切片和管道，不能用于 map）</td></tr><tr><td align="left">new、make</td><td align="left">new 和 make 均是用于分配内存：  
new 用于值类型和用户定义的类型，如自定义结构；  
make 用于内置引用类型（切片、map 和管道）。  
它们的用法就像是函数，但是将类型作为参数：new(type)、make(type)。  
new(T) 分配类型 T 的零值并返回其地址，也就是指向类型 T 的指针。  
它也可以被用于基本类型：v := new(int)。make(T) 返回类型 T 的初始化之后的值，因此它比 new 进行更多的工作，new() 是一个函数，不要忘记它的括号</td></tr><tr><td align="left">copy、append</td><td align="left">用于复制和连接切片</td></tr><tr><td align="left">panic、recover</td><td align="left">两者均用于错误处理机制</td></tr><tr><td align="left">print、println</td><td align="left">底层打印函数，在部署环境中建议使用 fmt 包</td></tr><tr><td align="left">complex、real imag</td><td align="left">用于创建和操作复数</td></tr></tbody></table>

- - - - - -

- - - - - -

- - - - - -

##### **`defer`**

1. 关键字 **`defer`** 的用法类似于面向对象编程语言 Java 和 C# 的 **`finally`** 语句块，它一般用于释放某些已分配的资源。
2. 当有多个 **`defer`** 行为被注册时，它们会以逆序执行（类似栈，即后进先出）
3. 与**[闭包](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/06.8.md#68-%E9%97%AD%E5%8C%85 "闭包")**配合使用
4. **在函数`return`后执行**

```go
package main

import (
    "fmt"
)

// 测试一
func main() {
    for i := 0; i 
```

- - - - - -

 **[用 defer 关闭文件](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/12.7.md#127-%E7%94%A8-defer-%E5%85%B3%E9%97%AD%E6%96%87%E4%BB%B6 "用 defer 关闭文件")**

```go
func data(name string) string {
    f, _ := os.OpenFile(name, os.O_RDONLY, 0)
    defer f.Close()           // 在函数return后执行
    contents, _ := ioutil.ReadAll(f)
    return string(contents)
}

```

在函数 **return 后**执行了 **f.Close()**

- - - - - -

- - - - - -

- - - - - -

##### 异常处理 **`panic`** 、**`recover`**

- **`panic`** : Go语言中没有类似Java语言中的Exception，而是使用 panic
- **`recover`** ：Go 语言还提供了 `recover` 函数，可以避免因为 `panic` 发生而导致整个程序终止，`recover` 函数只在 `defer` 中生效

**示例**

```go
package main

import "fmt"

func main() {
    f()
    fmt.Println("f()函数执行结束")
}

func f() {
    defer func() {
        if r := recover(); r != nil {
            fmt.Println("捕获可能发生的异常: ", r)
        }
    }()

    fmt.Println("准备进入g()函数")
    g()
    fmt.Println("g()函数执行结束")
}

func g() {
    defer fmt.Println("执行 defer g()函数")
    fmt.Println("进入g()函数")
    panic(fmt.Sprint("g()函数引发异常"))
}


```

```
准备进入g()函数
进入g()函数
执行 defer g()函数
捕获可能发生的异常:  g()函数引发异常
f()函数执行结束

```

- **`panic`** 会导致栈被展开直到 **`defer`** 修饰的 **`recover()`** 被调用或者**`程序中止`**。([官方文档](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/13.3.md#133-%E4%BB%8E-panic-%E4%B8%AD%E6%81%A2%E5%A4%8Drecover "官方文档")) 
  - **通俗的理解**就是一但发生了异常，栈就会停止继续执行指令，并且优先查找是否有 **`recover()`**，如果找到了就进行恢复，如果没有找到就直接中止程序运行。

**[最佳实践](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/13.4.md#134-%E8%87%AA%E5%AE%9A%E4%B9%89%E5%8C%85%E4%B8%AD%E7%9A%84%E9%94%99%E8%AF%AF%E5%A4%84%E7%90%86%E5%92%8C-panicking "最佳实践")**

- 这是所有自定义包实现者应该遵守的最佳实践： 
  1. 在包内部，总是应该从 panic 中 recover：不允许显式的超出包范围的 panic()
  2. 向包的调用者返回错误值（而不是 panic）。
- 在包内部，特别是在非导出函数中有很深层次的嵌套调用时，**将 `panic` 转换成 `error`** 来告诉调用方为何出错，是很实用的，**且提高了代码可读性**。

```go
package src

import (
    "fmt"
)

// 自定义抛出异常
func CalcDiv(a, b int) (i int, err error) {
    if b == 0 {
        // 1. 用 errors 创建错误对象
        //err = errors.New("除数不能为0")
        // 2. 用 fmt 创建错误对象
        err = fmt.Errorf("除数不能为0")
        return
    }
    return a / b, err
}


```

```go
package main

import (
    "Test/src"
    "fmt"
)

// 使用
func main() {
    _, err := src.CalcDiv(6, 0)
    if err != nil {
        fmt.Println(err)
    }
}


```

- - - - - -

- - - - - -

- - - - - -

##### **[值类型和引用类型](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/4468f9ff3a49868ce1033055101113284efc5679/eBook/04.4.md#442-%E5%80%BC%E7%B1%BB%E5%9E%8B%E5%92%8C%E5%BC%95%E7%94%A8%E7%B1%BB%E5%9E%8B "值类型和引用类型")**

 程序中所用到的内存在计算机中使用一堆箱子来表示（这也是人们在讲解它的时候的画法），这些箱子被称为 `"字"`。根据不同的处理器以及操作系统类型，所有的字都具有 32 位（4 字节）或 64 位（8 字节）的相同长度；所有的字都使用相关的内存地址来进行表示（以十六进制数表示）。  
 所有像 **int、float、bool 和 string** 这些基本类型**都属于`值类型`**，使用这些类型的变量直接指向存在内存中的值：  
[![](http://qiniu.dev-share.top/image/jpg/golang_fig4.1.jpg)](http://qiniu.dev-share.top/image/jpg/golang_fig4.1.jpg)

- - - - - -

 另外，像数组（**`[]`**）和结构（**`struct`**）这些复合类型也是值类型。  
 当使用等号 **`=`** 将一个变量的值赋值给另一个变量时，如：**`j = i`**，实际上是在内存中将 **`i`** 的值进行了**`拷贝`**：  
[![](http://qiniu.dev-share.top/image/jpg/golang_fig4.2.jpg)](http://qiniu.dev-share.top/image/jpg/golang_fig4.2.jpg)

- - - - - -

 你可以通过 **`&i`** 来获取变量 **`i`** 的内存地址，例如：**`0xf840000040`**（每次的地址都可能不一样）。**值类型的变量的值`存储在栈中`**。  
 内存地址会根据机器的不同而有所不同，甚至相同的程序在不同的机器上执行后也会有不同的内存地址。因为每台机器可能有不同的存储器布局，并且位置分配也可能不同。  
 更复杂的数据通常会需要使用多个字，这些数据一般使用引用类型保存。  
 一个引用类型的变量 **`r1`** 存储的是 **`r1`** 的值所在的内存地址（数字），或内存地址中第一个字所在的位置。  
[![](http://qiniu.dev-share.top/image/jpg/golang_fig4.3.jpg)](http://qiniu.dev-share.top/image/jpg/golang_fig4.3.jpg)

- - - - - -

 这个**内存地址**被称之为**`指针`**（你可以从上图中很清晰地看到），这个指针实际上也被存在另外的某一个字中。  
 同一个引用类型的指针指向的多个字可以是在连续的内存地址中（内存布局是连续的），这也是计算效率最高的一种存储形式；也可以将这些字分散存放在内存中，每个字都指示了下一个字所在的内存地址。  
 当使用赋值语句 **`r2 = r1`** 时，只有引用（地址）被复制。  
 如果 **`r1`** 的值被改变了，那么这个值的所有引用都会指向被修改后的内容，在这个例子中，**`r2`** 也会受到影响。  
 在 **`Go`** 语言中，**`指针`属于引用类型** ，其它的引用类型还包括 **slices，maps和 channel**。**被引用的变量会`存储在堆中`**，以便进行垃圾回收，且比栈拥有更大的内存空间。

- - - - - -

- - - - - -

- - - - - -

##### 字符串

- 在**Java**语言中 **`String.class`** 表示为字符串类型，它是一个类，是**引用类型**
- 在**Go**语言中 **`type string string`** 表示为字符串类型，它是一个类型，是一种**值类型**，且`值不可变`，即创建某个文本后你无法再次修改这个文本的内容；更深入地讲，字符串是 **字节的`定长数组`** 。**[详见官方文档](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/04.6.md#46-%E5%AD%97%E7%AC%A6%E4%B8%B2 "详见官方文档")**

- - - - - -

- - - - - -

- - - - - -

##### 指针

 程序在内存中存储它的值，每个内存块（或字）有一个地址，通常用十六进制数表示，如：`0x6b0820` 或 `0xf84001d7f0`。  
 **`Go`** 语言的取地址符是 **`&`** ，放到一个变量前使用就会返回相应变量的内存地址，这个地址可以存储在一个叫做 **指针的`特殊数据类型`** 中。  
 **一个指针变量可以指向任何一个值的内存地址** 它指向那个值的内存地址，在 32 位机器上占用 4 个字节，在 64 位机器上占用 8 个字节，并且与它所指向的值的大小无关。当然，可以声明指针指向任何类型的值来表明它的原始性或结构性；你可以在指针类型前面加上 **`*`** 号（前缀）来获取指针所指向的内容，这里的 **`*`** 号是一个类型更改器。使用一个指针引用一个值被称为间接引用。  
 当一个指针被定义后没有分配到任何变量时，它的值为 **`nil`** 。  
 一个指针变量通常缩写为 **`ptr`** 。

###### **注意事项**

 在书写表达式类似 **`var p *type`** 时，切记在 **`*`** 号和 **`指针`** 名称间留有一个空格，因为 **`- var p*type`** 是语法正确的，但是在更复杂的表达式中，它容易被误认为是一个乘法表达式！  
 符号 **`*`** 可以放在一个指针前，如 **`*intP`**，那么它将得到这个指针指向地址上所存储的值；这被称为反引用（或者内容或者间接引用）操作符；另一种说法是指针转移。

 如果传递给函数的是一个指针，指针的值（**`一个地址`**）会被复制，但指针的值所指向的地址上的值不会被复制；我们可以通过这个指针的值来修改这个值所指向的地址上的值。  
 **指针也是变量类型，`有自己的地址和值`，通常指针的值指向一个变量的地址。所以传递指针，既是按引用传递也是按值传递。**  
 几乎在任何情况下，传递指针（一个32位或者64位的值）的消耗都比传递副本来得少。

**[详见官方文档](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/04.9.md#49-%E6%8C%87%E9%92%88 "详见官方文档")**

- - - - - -

- - - - - -

- - - - - -

##### 函数

 如果需要申明一个在外部定义的函数，你只需要给出函数名与函数签名，不需要给出函数体：

```go
func flushICache(begin, end uintptr) // implemented externally

```

 函数也可以以申明的方式被使用，作为一个函数类型，就像：

```go
type binOp func(int, int) int

```

 在这里，不需要函数体 {}。  
 函数是一等值（first-class value）：它们可以赋值给变量，就像 add := binOp 一样。  
 这个变量知道自己指向的函数的签名，所以给它赋一个具有不同签名的函数值是不可能的。

 **`Go 默认使用按值传递`** 来传递参数，也就是传递参数的副本。

```go
// 函数类型的作用，
// 在JavaScript中我们写一个回调函数，只需要一个变量即可，因为它是弱类型
// 在Go语言中，在使用回调函数时，要先定义回调函数类型

// 1. 预 定义计算器的返回结果类型，没有实际逻辑体
type Result func(int)

// -----------------------------------

// 2. 实现计算器功能，以回调函数的形式，封装逻辑
func Calc(p1 int, p2 int, rest Result) {
    // 2.1 计算逻辑
    rest(p1 + p2)
}

// -----------------------------------

// 3. 测试
func main() {
    // 执行计算
    Calc(1, 2, func(callParam int) {
        // 接收返回结果
        fmt.Println(callParam)
    })
}


```

- - - - - -

###### **实际应用**

```go
package main

import (
    "fmt"
    "io/ioutil"
    "net/http"
)

// 1. 定义一个名为 Options 的类型
type Options struct {
    url     string            // 定义 网址变量
    success func(interface{}) // 定义 请求成功后回调函数
    errors  func(err error)   // 定义 请求失败后回调函数
}

// -----------------------------------

// 2. 将Options 类型，做为参数限制，进行逻辑封装
func ajax(o *Options) {

    // 2.1 发起http请求
    resp, err := http.Get(o.url)
    if err != nil {
        // 2.1.1 将异常信息告诉使用者
        o.errors(err)
    }

    // 2.4 defer 最后关闭请求
    defer resp.Body.Close()

    // 2.2 获取响应数据
    body, err := ioutil.ReadAll(resp.Body)
    if err != nil {
        // 2.2.1 将异常信息告诉使用者
        o.errors(err)
    }
    // 2.3 将成功信息告诉使用者
    o.success(string(body))
}

// -----------------------------------

// 3. 测试
func main() {
    ajax(&Options{
        url: "http://www.baidu.com",
        success: func(i interface{}) {
            fmt.Println(i)
        },
        errors: func(err error) {
            fmt.Println(err)
        },
    })
}


```

- - - - - -

- - - - - -

- - - - - -

##### 数组

###### **[概念](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/07.1.md#711-%E6%A6%82%E5%BF%B5 "概念")**

 数组是具有相同 **`唯一类型`** 的一组已编号且**长度固定**的数据项序列（这是一种同构的数据结构）；这种类型可以是任意的原始类型例如整型、字符串或者自定义类型。数组长度必须是一个常量表达式，并且**必须是一个非负整数**。数组长度也是数组类型的一部分，所以 **`[5]int`** 和 **`[10]int`** 是属于不同类型的。**数组长度最大为 `2GB`**

<table><thead><tr><th align="left"></th><th align="left"></th><th align="left"></th><th align="left"></th></tr></thead><tbody><tr><td align="left">数组</td><td align="left">**`var arr [number]type`**</td><td align="left">var arr \[6\]int  
arr\[0\] = 1  
arr\[1\] = 2  
arr\[2\] = 3  
arr\[3\] = 4  
arr\[4\] = 5</td><td align="left">创建一个长度为6的数组，它的值为 `1` `2` `3` `4` `5` `0`，最后一位的`0`为默认值</td></tr><tr><td align="left">数组</td><td align="left">**`var arr [...]type`**</td><td align="left">var arr \[...\]int  
arr\[0\] = 1  
arr\[1\] = 2  
arr\[2\] = 3  
arr\[3\] = 4  
arr\[4\] = 5</td><td align="left">数组不能使用 **`[...]`** 这样写，只有数组常量才可以这样写，虽然编译时通过，但会引发运行时异常**`use of [...] array outside of array literal`**</td></tr><tr><td align="left">数组常量</td><td align="left">**`[number]type{}`**</td><td align="left">arr := \[6\]int{1, 2, 3, 4, 5}</td><td align="left">创建一个长度为6的数组，它的值为 `1` `2` `3` `4` `5` `0`，最后一位的`0`为默认值</td></tr><tr><td align="left">数组常量</td><td align="left">**`[...]type{}`**</td><td align="left">arr := \[...\]int{1, 2, 3, 4, 5}</td><td align="left">创建一个未知长度的数组，它的最终长度是由数组中初始化的值的数量来决定</td></tr></tbody></table>

- - - - - -

##### 切片(Slice)

 **把数组分片，即为`切片`。**

###### **[概念](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/07.2.md#721-%E6%A6%82%E5%BF%B5 "概念")**

- 切片和数组不同的是，切片的长度可以在运行时修改，最小为 0 最大为相关数组的长度：切片是一个 **`长度可变的数组`**。
- **多个切片如果表示同一个数组的片段**，它们可以**共享数据**；因此一个切片和相关数组的其他切片是**共享存储**的，相反，不同的数组总是代表不同的存储。数组实际上是切片的构建块。
- **`优点`** 因为切片是引用，所以它们不需要使用额外的内存并且比使用数组更有效率，所以在 Go 代码中切片比数组更常用。
- 声明切片的格式是： **`var identifier []type`**（不需要说明长度）。
- 一个切片在未初始化之前默认为 nil，长度为 0。
- 切片的初始化格式是：**`var slice1 []type = arr1[start:end]`**。  
  这表示 slice1 是由数组 arr1 从 start 索引到 end-1 索引之间的元素构成的子集（**切分数组**，**`start:end` 被称为 `slice` 表达式**）。所以 slice1\[0\] 就等于 arr1\[start\]。这可以在 arr1 被填充前就定义好。 
  - **[不需要将一个指向切片的指针传递给函数](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/16.5.md#165-%E4%B8%8D%E9%9C%80%E8%A6%81%E5%B0%86%E4%B8%80%E4%B8%AA%E6%8C%87%E5%90%91%E5%88%87%E7%89%87%E7%9A%84%E6%8C%87%E9%92%88%E4%BC%A0%E9%80%92%E7%BB%99%E5%87%BD%E6%95%B0 "不需要将一个指向切片的指针传递给函数")**
      - 切片实际是一个指向潜在数组的指针。我们常常需要把切片作为一个参数传递给函数是因为：实际就是传递一个指向变量的指针，在函数内可以改变这个变量，而不是传递数据的拷贝。  
            **因此应该这样做：**  
            `func findBiggest( listOfNumbers []int ) int {}`  
            **而不是：**  
            `func findBiggest( listOfNumbers *[]int ) int {}`  
            **`当切片作为参数传递时，切记不要解引用切片。`**

- - - - - -

<table><thead><tr><th align="left"></th><th align="left"></th><th align="left"></th><th align="left"></th></tr></thead><tbody><tr><td align="left">切片</td><td align="left">**`var slice1 []type = arr[start:end]`**</td><td align="left">arr := \[\]int{1, 2, 3, 4, 5, 6}</td><td align="left">一个由数字 **1、2、3、4、5、6** 组成的切片可以这么生成：**`arr := [6]int{1, 2, 3, 4, 5, 6}[:]`**  
(解释：先用`arr := [6]int{1, 2, 3, 4, 5, 6}`生成数组， 再使用**`arr[:]`转成切片**) 更简单的写法 **`arr := []int{1, 2, 3, 4, 5, 6}`** **`arr2 := arr[:]`** 是用切片组成的切片，拥有相同的元素，但是仍然**指向相同的相关数组**。

</td></tr><tr><td align="left">用 make() 创建一个切片</td><td align="left">**`var slice1 []type = make([]type, len)`**   
 也可以简写为 **`slice1 := make([]type, len)`**，这里 len 是数组的长度并且也是 slice 的初始长度。</td><td align="left">make(\[\]int, 50, 100)</td><td align="left">当相关数组还没有定义时，我们可以使用 make() 函数来创建一个切片，同时创建好相关数组   
make 的使用方式是：**`func make([]T, len, cap)`**，其中 cap 是可选参数。</td></tr></tbody></table>

```go
package main

import "fmt"

func main() {
    // 定义string类型的切片，其初始化后的数据为{"a", "b", "c", "d", "e", "f", "g"}
    arr := []string{"a", "b", "c", "d", "e", "f", "g"}
    // 切片用法
    // s := arr[startIndex:endIndex] 将 arr 中从下标 startIndex 到 endIndex-1 下的元素创建为一个新的切片。
    // s := arr[startIndex:]         默认 endIndex 时将表示一直到arr的最后一个元素。
    // s := arr[:endIndex]           默认 startIndex 时将表示从 arr 的第一个元素开始。
    s := arr[1:4]
    fmt.Println(s) // [b c d]
}


```

- - - - - -

###### 复制切片

 **`func copy(dst, src []T) int`** copy 方法将类型为 T 的切片从源地址 src 拷贝到目标地址 dst，覆盖 dst 的相关元素，并且返回拷贝的元素个数。源地址和目标地址可能会有重叠。**拷贝个数是 src 和 dst 的`长度最小值`**。如果 src 是字符串那么元素类型就是 byte。

```go
package main

import "fmt"

func main() {

    // 定义数组常量
    arr := []int{1, 2, 3, 4, 5, 6, 7, 8, 9, 10}
    // index     0  1  2  3  4  5  6  7  8  9

    // 切片 a1，重新申请内存
    a1 := make([]int, 2)
    // a1 := []int{6, 6} // 结果是一样的，因为会被arr的数据覆盖
    copy(a1, arr[6:8])
    fmt.Println("a1的值:", a1, "    a1的长度", len(a1)) // a1的值: [7 8]     a1的长度 2

}

```

- - - - - -

- - - - - -

- - - - - -

##### make()与new()的区别

 在golang有两个关键字，刚开始学golang很容易搞混，**[详见官方文档](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/07.2.md#724-new-%E5%92%8C-make-%E7%9A%84%E5%8C%BA%E5%88%AB "详见官方文档")**

##### **new**

 new可以用来初始化类型，并返回内存地址，需要注意的是被new初始化的类型，类型中所有的属性都会被设置 **`"预设值"`** ，例如

- 字符串的预设值为 `""`
- number的预设值为 `0`
- channel, func, map, slice 等等则会是 `nil`

 正是因为这个特性，在某些情况下会带来问题，例如:

```go
func main() {
    people := new(map[string]string)
    p := *people
    p["name"] = "Kalan" // panic: assignment to entry in nil map
}

```

 引发问题的原因是因为new初始化的map的默认值是 nil map**因此需要改为make()**

##### **make**

```go
func main() {
    people := make(map[string]string)
    people["name"] = "Kalan"
    fmt.Println(people["name"])
}

```

 make与new不同，make是用来初始化一些特别的类型，例如channel, func, map, slice 等等，还有一个区别是make创建的初始化的类型， **不会返回内存地址**

- - - - - -

- - - - - -

- - - - - -

##### map

 **`注意`：map** 不是按照 key 的顺序排列的，也不是按照 value 的序排列的。  
 **译者注**：map的本质是散列表，而map的增长扩容会导致重新进行散列，这就可能使map的遍历结果在扩容前后变得不可靠，Go设计者为了让大家不依赖遍历的顺序，每次遍历的起点--即起始bucket的位置不一样，即不让遍历都从bucket0开始，所以即使未扩容时我们遍历出来的map也总是**`无序的`**。

###### **[概念](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/08.1.md#811-%E6%A6%82%E5%BF%B5 "概念")**

 map 是引用类型，可以使用如下声明：

```go
var map1 map[keytype]valuetype
var map1 map[string]int

```

- 未初始化的 map 的值是 **`nil`**。
- **key** 可以是任意可以用 `==` 或者 `!=` 操作符比较的类型，比如 string、int、float。所以**数组、切片和结构体不能作为 key** (译者注：含有数组切片的结构体不能作为 key，只包含内建类型的 struct 是可以作为 key 的），但是指针和接口类型可以。
- **value** 可以是任意类型的；
- map 是 **引用类型** 的： 内存用 **make** 方法来分配。
- map 的初始化：`var map1 = make(map[keytype]valuetype)`。或者简写为：`map1 := make(map[keytype]valuetype)`。

```go
// 测试基本类型做为map的值
func main() {
    map1 := map[string]int{"a": 1}
    fmt.Println(map1["a"])        // 如果key不存在，它会返回value类型的 空值
}


// 测试函数做为map的值
func main() {

    // 正常声明
    map1 := make(map[string]func() string)
    map1["a"] = func() string { return "hello" }
    map1["b"] = func() string { return "world" }
    fmt.Println(map1["a"](), map1["b"]())

    fmt.Println("----------------------")

    // 简写声明
    map2 := map[string]func() string{
        "a": func() string { return "hello" },
        "b": func() string { return "world" },
    }

    for k, v := range map2 {
        fmt.Println(k, v())
    }
}


```

- 不要使用 new，永远用 make 来构造 map
- 注意 如果你错误地使用 new() 分配了一个引用对象，你会获得一个空引用的指针，相当于声明了一个未初始化的变量并且取了它的地址

- - - - - -

##### **[map 的排序](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/08.5.md#85-map-%E7%9A%84%E6%8E%92%E5%BA%8F "map 的排序")**

- map 默认是无序的，不管是按照 key 还是按照 value 默认都不排序
- 如果你想为 map 排序，需要将 key（或者 value）拷贝到一个切片，再对切片排序，然后可以使用切片的 for-range 方法打印出所有的 key 和 value。  
  但是如果你想要一个排序的列表，那么最好使用结构体切片，这样会更有效：

```go
type name struct {
    key string
    value int
}

```

- - - - - -

- - - - - -

- - - - - -

##### **[为自定义包使用 godoc](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/09.6.md#96-%E4%B8%BA%E8%87%AA%E5%AE%9A%E4%B9%89%E5%8C%85%E4%BD%BF%E7%94%A8-godoc "为自定义包使用 godoc")**

注释必须以 **`//`** 开始并无空行放在声明（包，类型，函数）前。godoc 会为每个文件生成一系列的网页。

```ruby
go-proejct
.
│  go.mod
│  go.sum
│  main.go
│
├─gee
│      context.go
│      gee.go
│      go.mod
│      logger.go
│      README.md
│      router.go
│      trie.go
│
└─src                # 这个目录必须要有，否则会报错： cannot find package "." in:        \src


```

```ruby
## 安装doc工具
go get golang.org/x/tools/cmd/godoc

## 运行
godoc -http=:6060 -goroot="."

## 浏览器访问
http://localhost:6060/pkg/


```

- - - - - -

- - - - - -

- - - - - -

##### **[结构体定义](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/10.1.md#101-%E7%BB%93%E6%9E%84%E4%BD%93%E5%AE%9A%E4%B9%89 "结构体定义")**

```go
type Test struct{ x, y int }

```

##### 下图说明了结构体类型实例和一个指向它的指针的内存布局：

 **使用 new 初始化**：  
[![](http://qiniu.dev-share.top/image/png/golang_struct_new_init.png)](http://qiniu.dev-share.top/image/png/golang_struct_new_init.png)

1. 初始化Test类型
2. 分配内存（在内存中为Test类型开辟空间，并赋上初始值）
3. 返回指向已分配内存的指针

- - - - - -

 **作为结构体字面量初始化：**  
[![](http://qiniu.dev-share.top/image/png/golang_struct_const_init_01.png)](http://qiniu.dev-share.top/image/png/golang_struct_const_init_01.png)

1. 初始化Test类型
2. 分配内存（在内存中为Test类型开辟空间，并赋上初始值），直接返回已分配内存的**内存地址**

- - - - - -

[![](http://qiniu.dev-share.top/image/png/golang_struct_const_init_02.png)](http://qiniu.dev-share.top/image/png/golang_struct_const_init_02.png)  
 表达式 **`new(Type)`** 和 **`&Type{}` 是等价的**。  
 **混合字面量语法**（composite literal syntax）**`&struct1{a, b, c}`** 是一种简写，底层仍然会调用 **`new()`** ，这里值的顺序**必须按照字段顺序**来写。

- - - - - -

###### 实际应用

```go
package main

import "fmt"

type Address struct {
    number string
}

// 包含一个人的名字、地址编号、出生日期和图像
type VCard struct {
    *Address
    name     string
    birthday string
    image    string
}

func main() {

    // 优先初始化被引用的类型
    addr := &Address{"NO123456789"}

    card := &VCard{name: "张三", birthday: "2020", image: "docker"}
    card.Address = addr

    fmt.Println(*card)
    fmt.Println((*card.Address).number)

}

// {0xc000056230 张三 2020 docker}
// NO123456789

```

- - - - - -

- - - - - -

- - - - - -

##### **[带标签的结构体](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/10.4.md#104-%E5%B8%A6%E6%A0%87%E7%AD%BE%E7%9A%84%E7%BB%93%E6%9E%84%E4%BD%93 "带标签的结构体")**

- 结构体中的字段除了有名字和类型外，还可以有一个可选的标签**（tag）** ：它是一个附属于字段的字符串，可以是文档或其他的重要标记。
- 标签的内容**不可以在一般的编程中使用**，只有包 **`reflect`** 能获取它。

```go
package main

import (
    "fmt"
    "reflect"
)

type Address struct {
    number string
}

// 包含一个人的名字、地址编号、出生日期和图像
//   类型名称          tag标签
type VCard struct {
    *Address          "Address 匿名字段内嵌结构体类型"    // 匿名的字段(anonymous field)
    name     string   "姓名"
    birthday string   "生日"
}

func main() {

    vcard := &VCard{nil, "张三", "2020-02-40"}

    // 注意reflect.TypeOf(必须是结构体) 否则会引发异常 panic: reflect: Field of non-struct type *main.VCard
    class := reflect.TypeOf(*vcard)
    for i := 0; i ", ixField.Tag)
    }

}

// tag标签为:=> Address 匿名字段内嵌结构体类型
// tag标签为:=> 姓名
// tag标签为:=> 生日


```

- - - - - -

- - - - - -

- - - - - -

##### **[匿名字段内嵌结构体类型](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/10.5.md#1051-%E5%AE%9A%E4%B9%89 "匿名字段内嵌结构体类型")**

- 结构体可以包含一个或多个 **匿名（或内嵌）字段**，即这些字段没有显式的名字，只有字段的类型是必须的，此时**类型就是字段的名字**。匿名字段本身可以是一个结构体类型，即 **`结构体可以包含内嵌结构体`**。
- 可以粗略地将这个和面向对象语言中的继承概念相比较，随后将会看到它被用来模拟类似继承的行为。Go 语言中的继承是通过 **`内嵌`或`组合`** 来实现的，所以可以说，在 Go 语言中，相比较于继承，**组合更受青睐**。
- 提示：Go语言中 没有 `类`； Go语言最重要的三个方面分别是：封装、继承、多态，在 Go 中它们是以另一种形式表现的。
- 使用 **`匿名字段内嵌结构体类型`** 的这种用法被称为**`组合`**

- - - - - -

- - - - - -

- - - - - -

##### **[方法](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/10.6.md#106-%E6%96%B9%E6%B3%95 "方法")**

 在 Go 中，（接收者）类型关联的方法不写在类型结构里面，就像类那样；耦合更加宽松； **类型和方法之间的关联由`接收者`来建立** 。

 **定义方法的一般格式如下：**

```go
// func (recv 接收者类型) 方法名(参数) (返回值) { 方法体 }
func (recv receiver_type) methodName(parameter_list) (return_value_list) { ... }

```

- 鉴于性能的原因，**`recv`** 最常见的，是一个指向 **`receiver_type`的`指针`** （因为我们不想要一个实例的拷贝，如果按值调用的话就会是这样），特别是在 **`receiver`** 类型是结构体时，就更是如此了。

```go
// func (recv 接收者类型指针) 方法名(参数) (返回值) { 方法体 }
func (recv *receiver_type) methodName(parameter_list) (return_value_list) { ... }

```

- **`recv`** 就像是面向对象语言中的 **`this`** 或 **`self`**，但是 Go 中并没有这两个关键字。随个人喜好，**你可以使用 `this` 或 `self` 作为 `receiver` 的名字**。 
  - 但是Goland编译器会给出这样一个警告 **`Receiver has generic name`** 。将结构体的方法重命名为结构体的缩写。如`Client`结构体，可以命名为**`c`**或**`cl`**。
- **`指针方法`和`值方法`都可以在`指针`或`非指针`上被调用**

- - - - - -

- - - - - -

- - - - - -

##### **继承**

- 在 Go 中，没有像Java一样的继承关系，它是使用 **内嵌类型的方法实现继承**
- 当一个匿名类型被内嵌在结构体中时，匿名类型的可见方法也同样被内嵌，这在效果上等同于外层类型 **`继承`** 了这些方法：将父类型放在子类型中来实现亚型。这个机制提供了一种简单的方式来模拟经典面向对象语言中的子类和继承相关的效果。
- **内嵌**：将一个已存在类型的**字段和方法**注入到了另一个类型里：匿名字段上的方法 **`晋升`** 成为了**外层类型**的方法。当然类型可以有只作用于本身实例而不作用于内嵌 **`父`** 类型上的方法。
- 可以覆写方法：和内嵌类型方法具有同样名字的外层类型的方法**会覆写内嵌类型对应的方法**。

```go
package main

import (
    "fmt"
    "time"
)

// 1. 定义父类型
type Father struct{}
// 1.1 添加父类型方法
func (_ *Father) ShowTime() {
    fmt.Println("Father: ", time.Now())
}

// ------------------------------------------

// 2. 定义子类型
type Child struct {
    // *Father    // 内嵌的类型不需要指针
    Father        // 内嵌的类型
}

// 2.1 添加子类型方法
func (_ *Child) Hello() {
    fmt.Println("Child: Hello")
}

// 2.2 添加与父类型同名的 子类型方法
//func (_ *Child) ShowTime() {
//    fmt.Println("Child: ShowTime")
//}

// ------------------------------------------

// 3. 测试
func main() {
    child := &Child{}
    //child.Father.ShowTime() // 如果子类型中的方法与父类型中的方法名相同，那么需要明确指定
    child.ShowTime()
    child.Hello()
}


```

- - - - - -

###### **[聚合与内嵌](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/10.6.md#1066-%E5%A6%82%E4%BD%95%E5%9C%A8%E7%B1%BB%E5%9E%8B%E4%B8%AD%E5%B5%8C%E5%85%A5%E5%8A%9F%E8%83%BD "聚合与内嵌")**

- 什么是聚合？
  
  
  - **聚合** 也叫 **组合** ，包含一个所需功能类型的**具名字段**。
  
  ```go
  // 1. 定义父类型
  type Father struct{}
  // 2. 定义子类型
  type Child struct {
    father Father       // 内嵌的类型
  }
  
  ```
- 什么是内嵌？ 
  - **内嵌**， 所需功能类型是**匿名**的。
  - 内嵌的类型不需要指针
  - 因为一个结构体可以嵌入多个匿名类型，所以实际上我们可以有一个简单版本的**多重继承**
  - **多重继承** 实际上就是多个内嵌类型
  
  ```go
  // 1. 定义父类型
  type Father struct{}
  // 2. 定义子类型
  type Child struct {
    // *Father          // 内嵌的类型不需要指针
    Father              // 内嵌的类型
  }
  
  ```

- - - - - -

###### **[和其他面向对象语言比较 Go 的类型和方法](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/10.6.md#1069-%E5%92%8C%E5%85%B6%E4%BB%96%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1%E8%AF%AD%E8%A8%80%E6%AF%94%E8%BE%83-go-%E7%9A%84%E7%B1%BB%E5%9E%8B%E5%92%8C%E6%96%B9%E6%B3%95 "和其他面向对象语言比较 Go 的类型和方法")**

**总结**

- Go 不需要一个显式的类定义，如同 Java、C++、C# 等那样，相反地，**`类`** 是通过提供一组作用于一个共同类型的方法集来隐式定义的。类型可以是结构体或者任何用户自定义类型。
- 在 Go 中，**`类型`**就是**`类`** （数据和关联的方法）。Go 不知道类似面向对象语言的类继承的概念。继承有两个好处：代码复用和多态。
- 在 Go 中，代码复用通过 **`组合`** 和 **`委托`** 实现，**`多态`** 通过 **`接口`** 的使用来实现：有时这也叫 **`组件编程`（Component Programming）** 。

- - - - - -

- - - - - -

- - - - - -

##### 接口 interface

**`Go 的接口提供了更强大、却更简单的多态行为。`**

- Go 语言不是一种 **`传统`** 的面向对象编程语言：它里面没有类和继承的概念。
- 但是 Go 语言里有非常灵活的 **接口** 概念，通过它可以实现很多**面向对象**的特性。
- （按照约定，只包含一个方法的）接口的名字由方法名加 **`er`** 后缀组成，例如 **Print`er`**、**Read`er`**、**Writ`er`**、**Logg`er`**、**Convert`er`** 等等。 
  - 还有一些不常用的方式（当后缀 **`er`** 不合适时），比如 **Recover`able`**，此时接口名以 **`able`** 结尾，
  - 或者以 **`I`** 开头（像 .NET 或 Java 中那样）。
- Go 语言中的接口**都很简短**，通常它们会包含 0 个、最多 **3** 个方法。
- **`永远不要使用一个指针指向一个接口类型，因为它已经是一个指针。`**

1. **类型不需要显式声明它实现了某个接口：接口被隐式地实现。多个类型可以实现同一个接口。**
2. **实现某个接口的类型（除了实现接口方法外）可以有其他的方法。**
3. **一个类型可以实现多个接口。**
4. **接口类型可以包含一个实例的引用， 该实例的类型实现了此接口（接口是动态类型）。**

###### **接口的创建与使用**

```go
package main

import "fmt"

// 1. 定义接口
type Engine interface {
    // 接口中定义抽象方法
    Start()
    Stop()
}

// ------------------------------------------

// 2. 编写实现类
type Car struct {
}
// 2.1 此方法名称与接口中Start()方法相同，相当于实现了接口的Start()方法
func (c *Car) Start() {
    fmt.Println("Car 启动")
}
// 2.2 此方法名称与接口中Stop()方法相同，相当于实现了接口的Stop()方法
func (c *Car) Stop() {
    fmt.Println("Car 停止")
}

// ------------------------------------------

// 3. 实际使用，要求该方法的参数只能使用Engine接口类型
func foo(e Engine) {
    e.Start()
    e.Stop()
}

// ------------------------------------------

// 4. 测试
func main() {
    foo(&Car{})
}


```

- - - - - -

###### **[空接口](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/11.9.md#1191-%E6%A6%82%E5%BF%B5 "空接口")**

- **`interface{}`** 在Golang中没有Object这一说法，空接口`interface{}`类似 Java/C# 中所有类的基类：Object 类，二者的目标也很相近。可以给一个空接口类型的变量 **`var val interface {}`** 赋任何类型的值
- **`func Println(a ...interface{}) {}`** 参数中的 **`...`** 类似java、javascript、python等其它语言的形参
- **`a...`** 属性 **`...`** 类似Node.js中的解构赋值用法

```go
func Println(a ...interface{}) (n int, err error) {
    return Fprintln(os.Stdout, a...)
}

```

- - - - - -

###### 检测和转换接口变量的类型

```go
package main

import "fmt"

// 1. 定义一个接口类型
type interfaceI interface {
    Show()
}

// -----------------------

// 2. 定义用来测试的类型A
type structA struct {
}

func (a *structA) Show() {

}

// -----------------------

// 3. 定义用来测试的类型B
type structB struct {
}

func (b *structB) Show() {

}

// -----------------------

// 4. 检测和转换接口变量的类型
func main() {

    // 一个接口类型的变量 interfaceType 中可以包含任何类型的值，必须有一种方式来检测它的 动态 类型，即运行时在变量中存储的值的实际类型。

    // 创建一个接口类型的变量
    var interfaceType interfaceI

    // 转换接口变量的类型
    interfaceType = &structA{}
    // 检测变量的类型
    if _, ok := interfaceType.(*structA); ok {
        fmt.Println("------structA------")
    }

    // 转换接口变量的类型
    interfaceType = &structB{}
    // 使用 if-else 检测变量的类型
    if _, ok := interfaceType.(*structB); ok {
        fmt.Println("------structB------")
    }

}


```

- - - - - -

###### 类型判断：**[type-switch](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/11.4.md#114-%E7%B1%BB%E5%9E%8B%E5%88%A4%E6%96%ADtype-switch "type-switch")**

```go
var varI interface
// v := varI.(T)  // varI 必须是一个接口变量，否则编译器会报错
if _, ok := varI.(T); ok { // checked type assertion
    // ...
}


```

```go
// 检测和转换接口变量的类型
func main() {

    // 创建一个接口类型的变量
    var interfaceType interface

    // 转换接口变量的类型
    interfaceType = &structA{}
    // interfaceType = &structB{}

    // 使用 类型断言 加上 type-switch 检测变量的类型
    switch interfaceType.(type) {
    case *structA:
        fmt.Println("------structA------")
    case *structB:
        fmt.Println("------structB------")
    }

    // 使用 type-switch 检测变量的类型
    switch t := interfaceType.(type) {
    case *structA:
        fmt.Printf("------%T------\n", t)
    case *structB:
        fmt.Printf("------%T------\n", t)
    }

}


```

**使用接口完成多态的表现形式**

```go
package main

import (
    "fmt"
)

// IBean 定义接口
type IBean interface {
    Add() string
}

// ----------------------------------

type BeanImpl1 struct {
}

func (b *BeanImpl1) Add() string {
    return "hello world BeanImpl1"
}

// ----------------------------------

type BeanImpl22 struct {
}

func (b *BeanImpl22) Add() string {
    return "hello world BeanImpl22"
}

// ----------------------------------

// 测试抽象参数类型多态用法
func test1(bean interface{}) {
    b := bean.(IBean) // 接口类型强制转换，等同于 b := interface{}(bean).(IBean) 或 b := (bean).(IBean) 的写法
    fmt.Println(b.Add())
}

// 测试显示参数类型多态用法
func test2(b IBean) {
    fmt.Println(b.Add())
}

func main() {
    test1(&BeanImpl1{})  // hello world BeanImpl1
    test2(&BeanImpl22{}) // hello world BeanImpl22
}


```

- - - - - -

- - - - - -

- - - - - -

##### **[for 结构 无限循环](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/05.4.md#543-%E6%97%A0%E9%99%90%E5%BE%AA%E7%8E%AF "for 结构 无限循环")**

- 条件语句是可以被省略的，如 `i:=0; ; i++` 或 `for { }` 或 `for ;; { }`
  - （`;;` 会在使用 **gofmt** 时被移除）：这些循环的本质就是**`无限循环`** 。最后一个形式也可以被改写为 **`for true { }`**，但一般情况下都会直接写 **`for { }`**。
  - 如果 for 循环的头部**没有条件语句**，那么就会认为条件**永远为 true**，因此**循环体内必须有相关的条件判断**以确保会在某个时刻**退出循环**。

- - - - - -

- - - - - -

- - - - - -

##### **[反射](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/11.10.md#11101-%E6%96%B9%E6%B3%95%E5%92%8C%E7%B1%BB%E5%9E%8B%E7%9A%84%E5%8F%8D%E5%B0%84 "反射")**

```go
package main

import (
    "fmt"
    "reflect"
)

type T struct {
    A int
    B string
    c string // 首字母大写的字段为公有字段，只有公有访问权限的字段才可以被反射设置，如果反射进行设值，它将会抛出异常
}

// 可以被反射获取到
func (t T) Hi() {
    fmt.Println("Hi 方法被执行")
}

// 反射获取不到，因为方法为私有
func (t T) see() {
    fmt.Println("see 方法被执行")
}

// 反射获取不到，因为方法所属类型是指针
func (t *T) Show() {
    fmt.Println("Show 方法被执行")
}

func main() {
    t := &T{23, "skidoo", "AAA"} // &{23 skidoo AAA}
    fmt.Println("反射前原始值: ", t.A, t.B, t.c)

    //// 反射获取这个对象
    //class := reflect.ValueOf(t) // &{23 skidoo AAA}
    //// 获取这个指针指向的元素类型
    //element := class.Elem() // {23 skidoo AAA}
    // 简写，反射获取这个指针指向的元素类型
    element := reflect.ValueOf(t).Elem() // {23 skidoo AAA}

    // 使用反射操作 类型的属性与方法
    element.FieldByName("A").SetInt(10)  // 根据字段名称设置值
    element.Field(1).SetString("Hello")  // 根据字段索引位置设置值
    element.MethodByName("Hi").Call(nil) // 根据方法名称执行
    //element.Method(1) // 根据方法索引位置执行
    //v.Field(2).SetString("world") // 运行时异常 panic: reflect: reflect.Value.SetString using value obtained using unexported field

    fmt.Println("字段总数: ", element.NumField())
    fmt.Println("可被反射的方法数: ", element.NumMethod())
    fmt.Println("反射后新值: ", t.A, t.B, t.c)

}


```

- - - - - -

##### 实践-反射传参数对象，并返回对象切片

```go
package main

import (
    "encoding/json"
    "fmt"
    "reflect"
)

type Req struct {
    Name string
}

type Res struct {
    Name string
    Age  int
}

type T struct {
}

// Hi 可以被反射获取到
func (t *T) Hi(r *Req) []Res {
    fmt.Println("Hi 方法被执行:", r.Name)

    // 设置返回值
    res := make([]Res, 1)
    res[0] = Res{"大上海", 100000}
    return res
}

func main() {

    var t T

    objMethod := reflect.ValueOf(t.Hi)                        // 将方法包装为反射值对象
    paramList := []reflect.Value{reflect.ValueOf(&Req{"上海"})} // 构造方法的参数
    retList := objMethod.Call(paramList)                      // 反射调用函数，并接收返回值。到这里返回的结果不能进行【序列化、反序列化】
    obj := retList[0].Interface()                             // 所以需要调用.Interface()方法，这样返回的对象才能够被【序列化、反序列化】

    // 执行序化
    fmt.Println("\n执行序化")
    result, _ := json.Marshal(obj)
    fmt.Printf("%+v \n", string(result)) // [{"Name":"大上海","Age":100000}]

    // 执行反序化
    fmt.Println("\n执行反序化")
    var res []Res
    json.Unmarshal(result, &res)
    fmt.Printf("%+v \n", res) // [{Name:大上海 Age:100000}]
}


```

- - - - - -

- - - - - -

- - - - - -

###### **[总结：Go 中的面向对象](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/11.13.md#1113-%E6%80%BB%E7%BB%93go-%E4%B8%AD%E7%9A%84%E9%9D%A2%E5%90%91%E5%AF%B9%E8%B1%A1 "总结：Go 中的面向对象")**

- Go 没有类，而是松耦合的类型、方法对接口的实现。
- OO 语言最重要的三个方面分别是：封装，继承和多态，在 Go 中它们是怎样表现的呢？ 
  - **`封装`**（数据隐藏）：和别的 `OO` 语言有 4 个或更多的访问层次相比，Go 把它简化为了 2 层（参见 4.2 节的可见性规则）: 
      - 1）包范围内的：通过标识符**首字母`小写`**，对象 只在它所在的包内可见
      - 2）可导出的：通过标识符**首字母`大写`**，对象 对所在包以外也可见
- 类型只拥有自己所在包中定义的方法。 
  - **`继承`**：**用组合实现**：内嵌一个（或多个）包含想要的行为（字段和方法）的类型；多重继承可以通过内嵌多个类型实现
  - **`多态`**：**用接口实现**：某个类型的实例可以赋给它所实现的任意接口类型的变量。类型和接口是松耦合的，并且多重继承可以通过实现多个接口实现。Go 接口不是 Java 和 C# 接口的变体，而且接口间是不相关的，并且是大规模编程和可适应的演进型设计的关键。

- - - - - -

- - - - - -

- - - - - -

##### 高阶函数

 使用**高阶函数**，实际上就是**根据不同`参数`返回不同的`函数`**

```go
package main

import (
    "fmt"
)

type CarT struct {
    name   string // 名字
    config string // 配置
}

// 1. 我想编写一个动态生成函数的函数，我把它叫做函数工场，
//     工场可以生产不同的函数，但这些函数是有部分功能是相同的
func Car(c *CarT) func() {
    return func() {
        fmt.Println(c.name, c.config)
    }
}

// 2.1 制造卡车
var truck = Car(&CarT{name: "卡车", config: "低配"})

// 2.2 制造自行车
var bicycle = Car(&CarT{name: "自行车", config: "顶配"})

// 3. 测试
func main() {
    truck()
    bicycle()
}


```

- - - - - -

- - - - - -

- - - - - -

###### JSON 反序列化

`{"Name": "Wednesday", "Age": 6, "Parents": ["Gomez", "Morticia"]}`

```go
package main

import (
    "encoding/json"
    "fmt"
)

type Parents []string
// 定义与JSON中格式相同的结构类型，用来接收反序列化后的数据
type Project struct {
    Name string
    Age  int
    Parents
}

func main() {
    // 1. 定义JSON串
    b := []byte(`{"Name": "Wednesday", "Age": 6, "Parents": ["Gomez", "Morticia"]}`)
    // 2. 初始化结构对象
    p := &Project{}
    // 3. 执行反序列化操作，将JSON数据反序列化到结构对象中
    json.Unmarshal(b, p)
    fmt.Println(p)

    // 4. 执行序列化操作，将结构对象序列化为JSON数据结构
    resutl, _ := json.Marshal(p)
    fmt.Println(string(resutl))
}


```

- - - - - -

- - - - - -

- - - - - -

##### **[单元测试和基准测试](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/13.7.md#137-go-%E4%B8%AD%E7%9A%84%E5%8D%95%E5%85%83%E6%B5%8B%E8%AF%95%E5%92%8C%E5%9F%BA%E5%87%86%E6%B5%8B%E8%AF%95 "单元测试和基准测试")**

- 测试程序**必须属于被测试的包**，并且文件名满足这种形式 **`*_test.go`**，所以测试代码和包中的业务代码是分开的。如：**hello\_world`_test.go`**```
  .
  │  go.mod
  │  main.go
  │
  └─src
     hello_world.go          // 业务代码
     hello_world_test.go     // 测试代码
  
  ```
- **`_test`** 程序不会被普通的 **Go** 编译器编译，所以当放应用部署到生产环境时它们不会被部署；只有 **`gotest` 会编译所有的程序** ：普通程序和测试程序。
- **单元测试`Test`**: 测试文件中必须导入 **`testing`** 包，并写一些名字以 **`Test`Zzz** 打头的全局函数，这里的 **Zzz** 是被测试函数的字母描述，如 **`Test`FmtInterface**，**`Test`PayEmployees** 等。 
  - 测试函数必须有这种形式的头部： ```go
      func TestAbcde(t *testing.T)
      
      ```
  - **`T`** 是传给测试函数的结构类型，用来管理测试状态，支持格式化测试日志，如 **t.Log，t.Error，t.ErrorF** 等。在函数的结尾把输出跟想要的结果对比，如果不等就打印一个错误，成功的测试则直接返回。
- **基准测试`Benchmark`**: **`testing`** 包中有一些类型和函数可以用来做简单的基准测试；测试代码中必须包含以 **`Benchmark`Zzz** 打头的函数并接收一个 **`*testing.B`** 类型的参数，比如： ```go
  func BenchmarkReverse(b *testing.B) {
    ...
  }
  
  ```

- - - - - -

###### 实际应用

**hello\_world.go**

```go
package src

import (
    "fmt"
)

// 自定义抛出异常
func CalcDiv(a, b int) (i int, err error) {
    if b == 0 {
        // 1. 用 errors 创建错误对象
        //err = errors.New("除数不能为0")
        // 2. 用 fmt 创建错误对象
        err = fmt.Errorf("除数不能为0")
        return
    }
    return a / b, err
}

// 此函数除0并不会报错，因为类型是 float类型, (float32/float64结果都一样)
//func Calc1(a, b float32) float32 {
//    return a / b
//}


```

**hello\_world`_test`.go**

```go
package src

import (
    "testing"
)

// 创建测试函数，用来测试业务代码中的Calc()函数
func TestCalc(t *testing.T) {
    // 调用业务代码中的Calc()函数，执行业务代码的逻辑
    _, err := CalcDiv(6, 0)
    if err != nil {
        t.Log(err)
    }
}

// 创建测试函数，用来测试业务代码中的Calc()函数
func BenchmarkCalc(b *testing.B) {
    _, err := CalcDiv(6, 0)
    if err != nil {
        b.Log(err)
        b.Fail() // 标记测试函数为失败，然后继续执行（剩下的测试）。
    }
}


```

- - - - - -

- - - - - -

- - - - - -

##### 协程（goroutine）与通道（channel）

- **Go 原生支持应用之间的通信**（网络，客户端和服务端，分布式计算）和程序的**并发**，程序可以在不同的处理器和计算机上同时执行不同的代码段。
- **Go** 语言为构建并发程序的基本代码块是**协程 (goroutine) 与通道 (channel)** ，他们需要语言，编译器，和 runtime 的支持。
- **Go** 语言提供的垃圾回收器对并发编程至关重要。

**`不要通过共享内存来通信`，而是`通过通信来共享内存`。**  
**通信强制协作。**

- - - - - -

##### **[并发、并行和协程](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/14.1.md#141-%E5%B9%B6%E5%8F%91%E5%B9%B6%E8%A1%8C%E5%92%8C%E5%8D%8F%E7%A8%8B "并发、并行和协程")**

###### 什么是协程？

- 一个**应用程序是**运行在机器上的**一个进程**；**进程是**一个**运行在自己内存地址空间**里的**独立执行体**。
- 一个**进程**由一个或**多个**操作系统**线程组成**，这些线程其实是**共享同一个内存地址空间**的一起工作的执行体。 
  - 几乎所有`'正式'`的程序都是多线程的，以便让用户或计算机不必等待，或者能够同时服务多个请求（如 Web 服务器），或增加性能和吞吐量（例如，通过对不同的数据集并行执行代码）。
- 一个**并发程序**可以在**一个处理器**或者内核上使用多个线程来执行任务，但是只有 **`同一个程序`在某个时间点`同时运行`在多核或者`多处理器`** 上才是**真正的`并行`**。 
  - **`并行`** 是一种通过使用多处理器以提高速度的能力。
  - **通俗的讲(自己的理解)**，假设有一台**8核处理器**的电脑，早期的程序并发设计，是让其中的某一个处理器创建多个线程来执行任务，这样的操作并没有发挥出硬件的全部能力，只使用了**1/8**能力； 这里所讲的并行是可以让**8核处理器**每一个上都有这个程序的任务在执行，要发挥**8/8**的能力。

- **`并行`** 是一种通过使用**多处理器**以提高速度的能力。所以并发程序可以是并行的，也可以不是。

- 公认的，使用**多线程**的应用**难以做到准确**，最主要的问题是**内存中的数据共享**，它们会被多线程以**无法预知的方式进行操作**，导致一些无法重现或者随机的结果（称作 **`竞态`**）。 
  - **`不要`使用`全局变量`或者`共享内存`，它们会给你的代码在`并发运算的时候带来危险`。**
  - **解决之道**在于同步不同的线程，**对数据加锁**，这样同时就只有一个线程可以变更数据。不过过去的软件开发经验告诉我们**这会带来更高的复杂度**，更容易使代码出错以及**更低的性能**，所以这个经典的方法明显**不再适合**现代**多核/多处理器编程**：**thread-per-connection** 模型不够有效

- - - - - -

- Go 更倾向于其他的方式，在 Go 中，应用程序并发处理的部分被称作 **goroutines（协程）**，它可以进行更有效的并发运算。 
  - 在协程和操作系统线程之间并无一对一的关系：协程是根据一个或多个线程的可用性，映射（多路复用，执行于）在他们之上的；协程调度器在 Go 运行时很好的完成了这个工作。
- **协程**工作在**相同的地址空间**中，所以共享内存的方式一定是同步的；这个可以使用 sync 包来实现，不过我们**很不鼓励**这样做：Go 使用 **`channels`** 来同步协程。 
  - **协程** 可以 **运行在`多个`操作系统`线程`** 之间，也可以运行在**线程之内**，让你可以很小的内存占用就可以处理大量的任务。
  - **协程** 是通过使用关键字 **`go`** 调用（执行）一个函数或者方法来实现的（也可以是匿名或者 lambda 函数）。这样会在当前的计算过程中开始一个**同时进行的函数**，在**相同的地址空间**中并且**分配了独立的`栈`**，比如：**`go` sum(bigArray)**，在后台计算总和。
  - **协程** 的 **`栈`** 会根据需要进行伸缩，**不出现栈溢出**；开发者**不需要关心栈的大小**。当协程结束的时候，它会**静默退出**：用来启动这个协程的函数**不会得到任何的返回值**。
  - 任何 Go 程序都必须有的 **main()** 函数也可以看做是一个**协程**，尽管它并没有通过 go 来启动。协程可以在程序初始化的过程中运行（**在 `init()` 函数中**）。
  - 终止一个协程：**`runtime.Goexit()`**

- - - - - -

**[Go协程（goroutines）和协程（coroutines）](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/14.1.md#1415-go-%E5%8D%8F%E7%A8%8Bgoroutines%E5%92%8C%E5%8D%8F%E7%A8%8Bcoroutines "Go协程（goroutines）和协程（coroutines）")**  
（译者注：标题中的 **`Go` 协程** 即是 14 章讲的协程指的是 **Go 语言中的协程**。而 **协程（coroutines）** 指的是其他语言中的协程概念，仅在本节出现。）  
在其他语言中，比如 **C#，Lua 或者 Python 都有协程的概念**。这个名字表明它和 Go协程有些相似，不过有两点不同：

- **`Go` 协程** 意味着并行（或者可以以并行的方式部署），协程一般来说不是这样的
- **`Go` 协程** 通过通道来通信；协程通过让出和恢复操作来通信
- **`Go` 协程** 比协程更强大，也很容易从协程的逻辑复用到 Go 协程。

- - - - - -

- - - - - -

- - - - - -

##### **[协程间的信道](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/14.2.md#1421-%E6%A6%82%E5%BF%B5 "协程间的信道")**

- 协程可以使用 **共享变量** 来通信，但是 **`很不提倡`这样做**，因为这种方式给**所有的共享内存的多线程**都带来了**困难**。
- 而 Go 有一种特殊的类型，**通道（`channel`）**，就像一个可以用于发送类型化数据的管道，由其**负责协程之间的通信**，从而**避开所有**由**共享内存导致的陷阱**；这种通过通道进行通信的方式**保证了同步性**。 
  - **数据在通道中**进行传递：在任何给定时间，**一个数据被设计为`只有一个协程可以对其访问`**，所以**不会发生数据竞争**。 数据的所有权（可以读写数据的能力）也因此被传递。

[![](http://qiniu.dev-share.top/image/png/golang_channels_and_goroutines.png)](http://qiniu.dev-share.top/image/png/golang_channels_and_goroutines.png)

**声明通道：`var identifier chan datatype`未初始化的通道的值是 `nil` 。所有的类型都可以用于通道**

```go
package main

import "fmt"

func main() {
    // 语法： var identifier chan datatype
    // 声明了一个字符串通道 ch1，然后创建了它（实例化）
    // var ch1 chan string
    // ch1 = make(chan string)

    // 简写
    chInt := make(chan int)               // 构建一个 int 通道
    chStr := make(chan string)            // 构建一个 字符串 通道
    chFunc := make(chan func())           // 构建一个 函数 通道
    chChInt := make(chan chan int)        // 构建一个 int 通道的通道
    chInterface := make(chan interface{}) // 构建一个 接口 通道

    fmt.Println(chInt, chStr, chFunc, chInterface, chChInt)
}


```

- - - - - -

###### **通信操作符``**

- 为了可读性通道的命名通常以 **`ch`开头** 或者 **包含 `chan`** 。通道的**发送和接收都是原子操作**：它们总是**互不干扰**地完成。
- **``** 这个操作符直观的标示了数据的传输：信息按照箭头的方向流动。

```go
package main

import (
    "fmt"
    "runtime"
    "time"
)

func main() {
    // 1. 创建一个通道
    ch := make(chan string)

    // 2. 在协程中执行函数, (协程中的函数执行顺序是随机的)
    go sendData(ch)
    go getData(ch)

    // 输出协程数, -1 是因为默认的main()函数也是一个协程
    goroutineNum := runtime.NumGoroutine() - 1
    fmt.Printf("启动了 %v 个协程\n", goroutineNum)
    time.Sleep(6e9)
}

func sendData(ch chan string) {
    time.Sleep(2e9)
    fmt.Println("进入 sendData() 协程函数，开始第一次向通道中写入数据")
    ch ", input)
    }

    fmt.Println("程序运行结束！") // 猜猜我在什么时候执行？
}


```

- **main()** 函数中启动了两个协程：**sendData()** 通过通道 `ch` 发送了 `5` 个字符串，**getData()** 按顺序接收它们并打印出来。
- 如果 **`2`** 个协程需要通信，你**必须给他们同一个通道**作为参数才行。
- **`思考一下`：** 如果在写一个**getData1()** 函数， 多了一个消费者，又会怎么样呢？

- - - - - -

**[通道阻塞概念](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/14.2.md#1423-%E9%80%9A%E9%81%93%E9%98%BB%E5%A1%9E "通道阻塞概念")**

- 默认情况下，通信是同步且无缓冲的：在有接受者接收数据之前，发送不会结束。可以想象一个无缓冲的通道在没有空间来保存数据的时候：**必须要一个接收者准备好接收通道的数据然后发送者可以直接把数据发送给接收者**。所以通道的**发送/接收操作在对方准备好之前是`阻塞`的**： 
  - 1）**对于同一个通道**，**发送操作**（协程或者函数中的），**在接收者准备好之前是`阻塞`的**。
  - 2）**对于同一个通道**，**接收操作**是阻塞的（协程或函数中的），直到发送者可用：**如果通道中`没有数据`**，**接收者就`阻塞`了**。

- - - - - -

###### **[同步通道-使用带缓冲的通道](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/14.2.md#1425-%E5%90%8C%E6%AD%A5%E9%80%9A%E9%81%93-%E4%BD%BF%E7%94%A8%E5%B8%A6%E7%BC%93%E5%86%B2%E7%9A%84%E9%80%9A%E9%81%93 "同步通道-使用带缓冲的通道")**

```go
buf := 100
ch1 := make(chan string, buf)

```

**buf** 是通道可以同时容纳的元素（这里是 **string**）**个数**  
在缓冲满载之前（缓冲被全部使用之前），给一个**带缓冲的通道**发送数据是**不会阻塞**的，而从通道读取数据也不会阻塞，**直到缓冲空了**。

```go
ch :=make(chan type, value)

```

- `value == 0` -&gt; synchronous, unbuffered (阻塞）
- `value > 0` -&gt; asynchronous, buffered （非阻塞）取决于 value 元素
- 如果**容量大于 `0`**，通道就是异步的了：缓冲满载（发送）或变空（接收）之前**通信不会阻塞**，元素会按照发送的顺序被接收。 **`(非阻塞）`**
- 如果**容量是 `0`** 或者 **未设置**，通信 **仅在收发双方`准备好`** 的情况下才可以成功。 **`(阻塞）`**
- 使用通道的缓冲，你的程序会在 **`"请求"`** 激增的时候表现更好：更具弹性，专业术语叫：**更具有伸缩性**（scalable）。
- **但是**在**设计`算法`时首先考虑**使用 **`无缓冲`通道**，只在 **`不确定`的情况下使用缓冲**。

- - - - - -

###### **[无缓冲通道](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/14.2.md#1424-%E9%80%9A%E8%BF%87%E4%B8%80%E4%B8%AA%E6%88%96%E5%A4%9A%E4%B8%AA%E9%80%9A%E9%81%93%E4%BA%A4%E6%8D%A2%E6%95%B0%E6%8D%AE%E8%BF%9B%E8%A1%8C%E5%8D%8F%E7%A8%8B%E5%90%8C%E6%AD%A5 "无缓冲通道")**-**`死锁`**

- 通信是一种同步形式：通过通道，两个协程在通信中某刻同步交换数据。**无缓冲通道**成为了多个协程同步的完美工具。
- **无缓冲通道**甚至可以在**通道两端`互相阻塞`对方**，形成了叫做**死锁**的状态。Go 运行时会检查并 **`panic`** 停止程序。死锁几乎完全是由糟糕的设计导致的。

```go
// 场景一
func main() {
    ch := make(chan int)
    // 引发死锁的原因是，向通道发送信息时 [chan send]，会阻塞协程，导致main()协程无法继续运行
    ch 
```

- **无缓冲通道**会被阻塞，有两种方式可以避免这种情况：
  
  
  1. **设计无阻塞的程序**
  
  ```go
  func main() {
    ch := make(chan int)
    // 设计无阻塞的程序
    go func() {
        ch 
  ```
  
  
  2. **使用带缓冲的通道**
  
  ```go
  func main() {
    // 使用带缓冲的通道
    ch := make(chan int, 6)
    ch 
  ```

- - - - - -

###### 通道的方向

**通道类型可以用注解来表示它`只发送`或者`只接收`**

```go
package main

// 通道类型可以用注解来表示它只接收或者只发送
func main() {
    recv_only := make(chan
```

**实际应用**

```go
package main

import (
    "fmt"
    "strings"
    "time"
)

// 需求：使用通道创建乘法口诀表
// 创建两个通道，一个用来生成表格数据，一个用来输出表格数据

// 1. 生成表格数据(生产者)，限制通道只能发送数据
func create(ch chan
```

- - - - - -

###### **[关闭通道](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/14.3.md#143-%E5%8D%8F%E7%A8%8B%E7%9A%84%E5%90%8C%E6%AD%A5%E5%85%B3%E9%97%AD%E9%80%9A%E9%81%93-%E6%B5%8B%E8%AF%95%E9%98%BB%E5%A1%9E%E7%9A%84%E9%80%9A%E9%81%93 "关闭通道")**

- 只有在需要告诉接收者**不会再提供新的值的时候**，**才需要关闭通道**。只有**发送者**需要**关闭通道**，**接收者`永远不会需要`**。
- 在创建一个通道后使用 **`defer`** 语句是个不错的办法

```go
package main

func main() {
    // 创建一个通道
    ch := make(chan string)
    // 退出函数时关闭通道
    defer close(ch)
}

```

- - - - - -

###### **[使用 select 切换协程](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/14.4.md#144-%E4%BD%BF%E7%94%A8-select-%E5%88%87%E6%8D%A2%E5%8D%8F%E7%A8%8B "使用 select 切换协程")**

**语法**

```go
select {
case u:= 
```

- **`select`** 做的就是：选择处理列出的**多个通信**情况**中的一个**。 
  - 如果都阻塞了，会等待直到其中**一个**可以处理
  - 如果多个可以处理，**随机选择一个**
  - 如果没有通道操作可以处理并且写了 **`default`** 语句，它就会执行 **`default`** ，**`default`** 永远是可运行的（这就是准备好了，可以执行）。
  - 在 **`select`** 中使用发送操作并且有 **`default`** 可以确保发送不被阻塞！**如果没有 default，select 就会`一直阻塞`**。
  - **`select`** 语句实现了**一种监听模式**，**通常用在`无限循环`中**；在某种情况下，通过 **break** 语句使循环退出

**实际使用**

```go
package main

import (
    "fmt"
    "time"
)

// 生产者一
func ch1F(ch chan ", c1)
        case c2 :=  ", c2)
        case c3 :=  ", c3)
        default:
            fmt.Println("持续等待中......")
        }

    }
}

func main() {
    // 1. 创建三个通道
    ch1 := make(chan int)
    ch2 := make(chan string)
    ch3 := make(chan float64)

    // 2. 构建3个生产者，不断的向通道中写入数据
    go ch1F(ch1)
    go ch2F(ch2)
    go ch3F(ch3)

    // 3. 测试 select 的执行过程
    testSelect(ch1, ch2, ch3)
}


```

- - - - - -

**实际使用-[服务器模式](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/15.1.md#151-tcp-%E6%9C%8D%E5%8A%A1%E5%99%A8 "服务器模式")**

1. 监听操作系统端口，创建基于TCP协议的服务器端
2. 创建客户端，用来向服务器发送信息，并且收到响应
3. 监听通道中，客户端与服务器端交互数据的变化
4. 测试

```go
package main

import (
    "fmt"
    "net"
    "time"
)

// 自定义，定时器工具
func setInterval(ms time.Duration, f func()) {
    tick := time.Tick(ms)
    for {
        select {
        case  ", res)
        }
    }
}

// 4. 测试
func main() {

    // 4.1. 创建2个通道
    server := make(chan net.Conn)
    client := make(chan string)

    // 4.2. 通过监听操作系统端口实现基于TCP协议的服务器端
    go ListenServer(server)
    // 4.3. 实现TCP协议的客户端
    go setInterval(1e9, func() {
        go Client(client)
    })

    // 4.3. 监听通道中的数据变化
    ChanListen(server, client)
}


```

- - - - - -

###### 通道、超时和计时器

- 使用 **time.Tick(ms)** 模拟JavaScript的 **setInterval()**
- 使用 **time.After(ms)** 模拟JavaScript的 **setTimeout()**

```go
package main

import (
    "fmt"
    "time"
)

// 使用time.Tick(ms)模拟JavaScript的 setInterval()
func setInterval(ms time.Duration, f func()) {
    tick := time.Tick(ms)
    for {
        select {
        case 
```

- - - - - -

- - - - - -

- - - - - -

###### 协程和恢复（recover）

协程中的异常捕获

```go
package main

import (
    "fmt"
    "time"
)

func main() {

    // 1. 开启协程
    go func() {

        // 2. 捕获协程中可能会发生的异常
        defer func() {
            if err := recover(); err != nil {
                fmt.Println("协程中发生异常，已被捕获: --->", err)
            }
        }()

        // 3. 模拟：运行时异常
        for i := 3; i > -1; i-- {
            fmt.Println(1/i, 1%i)
        }

    }()

    // 等待运行时引发异常
    time.Sleep(2e9)

}


```

- - - - - -

- - - - - -

- - - - - -

###### **[怎么选择是该使用锁还是通道](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/14.7.md#147-%E6%96%B0%E6%97%A7%E6%A8%A1%E5%9E%8B%E5%AF%B9%E6%AF%94%E4%BB%BB%E5%8A%A1%E5%92%8Cworker "怎么选择是该使用锁还是通道")**

- 通道是一个较新的概念，本节我们着重强调了在 go 协程里通道的使用，但这**并不意味着**经典的**锁**方法**就不能使用**。
- go 语言让你可以根据实际问题进行选择：创建一个优雅、简单、可读性强、在大多数场景性能表现都能很好的方案。如果你的问题适合使用锁，也不要忌讳使用它。
- go 语言**注重实用**，什么方式最能解决你的问题就用什么方式，而**不是强迫**你使用**一种编码风格**。下面列出一个普遍的经验法则：
- **使用`锁`的情景**：
  
  
  - 访问共享数据结构中的缓存信息
  - 保存应用程序上下文和状态信息数据
- **使用`通道`的情景**： 
  - 与异步操作的结果进行交互
  - 分发任务
  - 传递数据所有权
- **当你发现**你的锁使用规则**变得很复杂**时，**可以反省使用通道**会不会使问题变得简单些。

- - - - - -

- - - - - -

- - - - - -

###### **[典型的客户端/服务器（C/S）模式](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/14.10.md#14101-%E5%85%B8%E5%9E%8B%E7%9A%84%E5%AE%A2%E6%88%B7%E7%AB%AF%E6%9C%8D%E5%8A%A1%E5%99%A8cs%E6%A8%A1%E5%BC%8F "典型的客户端/服务器（C/S）模式")**

- 使用 Go 的服务器通常会在协程中执行向客户端的响应，故而会对 **每一个客户端请求启动`一个协程`** 。一个常用的操作方法是**`客户端`请求自身中包含一个`通道`** ，而服务器则向这个通道发送响应。
- **`server`** 协程会无限循环以从 **`chan *Request`** 接收请求，并且为了避免被长时间操作所堵塞，它将为**每一个请求启动一个协程**来做具体的工作。  
  [![](http://qiniu.dev-share.top/image/png/golang_c_s.png)](http://qiniu.dev-share.top/image/png/golang_c_s.png)

- - - - - -

- - - - - -

- - - - - -

###### **[链式协程](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/14.12.md#1412-%E9%93%BE%E5%BC%8F%E5%8D%8F%E7%A8%8B "链式协程")**

**目标**，测试使用通道实现链式调用

1. 编写多个函数，用作链式调用
2. 测试调用多个函数，其执行结果是按顺序返回
3. stop通道一但接收到信号，将表示程序可以结束运行了

```go
package main

import (
    "fmt"
    "time"
)

// 目标，测试使用通道实现链式调用

// 1. 编写函数，用作链式调用
func step1(in chan int, out chan int) {
    time.Sleep(3e9) // 模拟业务处理耗时[3秒]
    // 1.1 阻塞通道，等待传入数据
    temp := ", temp)
    // 1.2 将数据传入下一个通道中，并且+1
    out ", temp)
    // 将数据传入下一个通道中，并且+1
    out ", temp)
    // 将数据传入下一个通道中，并且+1
    out ", s)
            endTime := time.Since(starTime)
            fmt.Println(endTime)
            // 结束程序
            return
        }
    }

}


```

**执行结果**

```
step1 ---> 1
step2 ---> 2
step3 ---> 3
停止 ---> 4
3.0018938s

```

- - - - - -

- - - - - -

- - - - - -

##### **[RPC远程调用](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/15.9.md#159-%E7%94%A8-rpc-%E5%AE%9E%E7%8E%B0%E8%BF%9C%E7%A8%8B%E8%BF%87%E7%A8%8B%E8%B0%83%E7%94%A8 "RPC远程调用")**

**先启动服务端，在启动客户端**

###### 服务端

```go
package main

import (
    "fmt"
    "net"
    "net/http"
    "net/rpc"
)

// 自定义类型
type Calc struct {
    N, M int
}

// 为自定义类型添加方法，执行乘法计算
func (t *Calc) Multiply(args *Calc, reply *int) error {
    fmt.Println("接收到客户端请求:", args)
    *reply = args.N * args.M
    return nil
}

func main() {
    // 初始化对象
    calc := new(Calc)
    // 将对象注册到rpc服务端，这样客户端就可以根据(对象名+方法名)进行远程访问
    rpc.Register(calc)
    rpc.HandleHTTP()
    // 使用TCP协议
    listener, _ := net.Listen("tcp", "localhost:1234")
    // 启动服务器
    go http.Serve(listener, nil)
    fmt.Println("服务器已启动")

    // 让服务器持续启动，直到使用stopServer通道停止服务
    stopServer := make(chan int)
    for {
        select {
        // 监听是否停止服务
        case 
```

**执行结果**

```
服务器已启动
接收到客户端请求: &{5 6}
接收到客户端请求: &{7 8}

```

- - - - - -

###### 客户端

```go
package main

import (
    "fmt"
    "net/rpc"
)

// 2. 同步调用
func SyncCall(client *rpc.Client) {
    // 使用匿名结构体做为参数(这里偷懒了不想定义参数对象类型)
    args := struct{ N, M int }{5, 6}
    var reply int
    // func (client *Client) Call(serviceMethod string, args interface{}, reply interface{}) error {...}
    // 客户端使用同步方法请求服务端，Call(服务端的类型名.方法名, 参数, 回调) error
    client.Call("Calc.Multiply", args, &reply)
    //
    fmt.Printf("Args: %d * %d = %d \n", args.N, args.M, reply)
}

// 3. 异步调用
func ASyncCall(client *rpc.Client) {
    // 使用匿名结构体做为参数
    args := struct{ N, M int }{7, 8}
    var reply int
    //func (client *Client) Go(serviceMethod string, args interface{}, reply interface{}, done chan *Call) *Call {
    // 客户端使用同步方法请求服务端，Go(服务端的类型名.方法名, 参数, 回调, 返回的通道) 返回的通道
    call := client.Go("Calc.Multiply", args, &reply, nil)
    // 执行完成后，返回的通道
    
```

**执行结果**

```
Args: 5 * 6 = 30
Args: 7 * 8 = 56

```

- - - - - -

- - - - - -

- - - - - -

##### **[基于网络的通道 netchan](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/15.10.md#1510-%E5%9F%BA%E4%BA%8E%E7%BD%91%E7%BB%9C%E7%9A%84%E9%80%9A%E9%81%93-netchan "基于网络的通道 netchan")** `未完待续`

- 备注：Go 团队决定改进并重新打造 netchan 包的现有版本，它已被移至 old/netchan。

- - - - - -

- - - - - -

- - - - - -

##### **[与 websocket 通信](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/15.11.md "与 websocket 通信")** `未完待续`

- 备注：Go 团队决定从 Go 1 起，将 websocket 包移出 Go 标准库，转移到 code.google.com/p/go 下的子项目 websocket，同时预计近期将做重大更改。

- - - - - -

- - - - - -

- - - - - -

##### **[使程序线程安全](https://github.com/unknwon/the-way-to-go_ZH_CN/blob/master/eBook/19.3.md#%E4%BD%BF%E7%A8%8B%E5%BA%8F%E7%BA%BF%E7%A8%8B%E5%AE%89%E5%85%A8)**