---
title: "Shell 常见用法"
date: "2018-07-24"
categories: 
  - "linux服务器"
  - "shell"
---

##### 写在最前面

- **`[]`** 和 **`test`**
    
    - 两者是一样的，在命令行里`test expr`和`[ expr ]`的效果相同。
- **`[[ ]]`**
    
    - 这是内置在shell中的一个命令
- **`let`** 和 **`(())`**
    
    - 两者基本上是一样的，双括号比`let`稍弱一些，主要进行算术运算

* * *

* * *

* * *

###### 大小定转换，替换特殊符号，并赋值给变量

```shell
#!/bin/bash
CONTEXT_NAME="abcd-efg"
# 环境变量名称，名称随便写
CONTEXT_NAME_ENV=$( echo $CONTEXT_NAME | tr 'a-z' 'A-Z' | tr '-' '_')

echo $CONTEXT_NAME_ENV
```

* * *

###### 字符串转数组

```shell
#!/bin/bash
# 测试：./generate_config.sh   msy=10.2.2.10  xyz=123.46.5.33

for i in "$@"; do
    if [ -n "$i" ]; then
        echo +------------------------+
        # 字符串拆分成数组，注意表达式后面要要空格
        array=(${i//=/ })
        # 按照数组下标输出
        echo ${array[0]}
        echo ${array[1]}
    fi
done

```

* * *

###### 这是首次学习shell时编写的代码，留个纪念

```shell
mao-siyu@pc:/mnt/1TB/devProject$ vim start.sh

#!/bin/bash
read -p "不许在说肥皂两个字:" INPUT
# 判断字符串是否存在
if [ $INPUT == "肥皂" ]
then
    echo "不要逼我删除你系统"
else
    echo "这样就对了!"
fi

mao-siyu@pc:/mnt/1TB/devProject$ ./start.sh
```

`#!/bin/sh` 是指此脚本使用/bin/sh来解释执行，#!是特殊的表示符，其后面跟的是此解释此脚本的shell的路径。

`$ cat /etc/shells` 可以查看系统支持的shell格式

其实第一句的#!是对脚本的解释器程序路径，脚本的内容是由解释器解释的，我们可以用各种各样的解释器来写对应的脚本。

比如说/bin/csh脚本，/bin/perl脚本，/bin/awk脚本，/bin/sed脚本,/bin/python脚本，甚至/bin/echo等等。

* * *

* * *

* * *

##### shell 常用命令

###### 1 `$* 与 $@ 区别`

test.sh

```shell
#!/bin/bash

echo "-- \$* 演示 ---"
for i in "$*"; do
    echo $i
done

echo "-- \$@ 演示 ---"
for i in "$@"; do
    echo $i
done
```

执行结果

```ruby
$ ./test.sh 1 2 3
-- $* 演示 ---
1 2 3
-- $@ 演示 ---
1
2
3
```

* * *

##### 2 map 用法

###### 输出所有的key

```ruby
echo ${!map[@]}
```

* * *

###### 输出所有value

```ruby
echo ${map[@]}
```

* * *

###### 输出map长度

```ruby
echo ${#map[@]}
```

* * *

###### 遍历所有的key

```ruby
for key in ${!map[@]};do
    echo $key
done
```

* * *

###### 遍历所有的value

```ruby
for val in ${map[@]};do
    echo $val
done
```

* * *

###### 遍历，根据key找到对应的value

```ruby
for key in ${!map[*]};do
    echo ${map[$key]}
done
```

* * *

###### `控制台获取参数， 动态获取map内容`

```shell
#!/bin/bash
# 测试：./test.sh 004 005

declare -A map=()
map["004"]="paas-login:1.0.0"
map["005"]="paas-system:1.0.0"

# 循环打印所有传入的参数
for i in "$@"; do
    # 判断 map取出的值不为空
    if [ -n "${map[$i]}" ]; then
        echo +------------------------+
        echo 所有key: "${!map[@]}"
        echo +------------------------+
        echo 所有value: "${map[@]}"
        echo +------------------------+
        echo -e "\033[36m 长度: ${#map[@]} \033[0m"
        echo +------------------------+
        echo -e "\033[36m ${map[$i]} \033[0m"
        echo +------------------------+
        echo

    fi
done

```

* * *

* * *

* * *

###### 3 使用正则灵活过滤

按指定内容过滤以`.jar`结尾的文件, 默认查询所有`.jar`文件

```shell
[hadoop@ipsen1 files]$ cat test-filter.sh
#!/bin/bash
dir=$(ls ../projects | grep $1.*.jar$)
for file in $dir
do
    echo $file
done
[hadoop@ipsen1 files]$

[hadoop@ipsen1 files]$
# 如果有参，就按参数过滤
[hadoop@ipsen1 files]$ ./test-filter.sh 48
48-ipsen-updateorginfo.jar

# 如果无参，就不过滤
[hadoop@ipsen1 files]$ ./test-filter.sh
01-saas-config-server.jar
02-saas-service-server.jar
04-saas-login.jar
05-saas-main.jar
```

* * *

###### 4 获取当前脚本的工作目录

```shell
cat > start.sh << ERIC
#!/bin/bash
# 获取 start.sh 文件所在目录的绝对路径
echo \$(cd \`dirname \$0\`; pwd)

# 进入 start.sh 文件所在的目录
cd \$(cd \`dirname \$0\`; pwd)

ERIC

```

* * *

* * *

* * *

###### 5 Shell 批量修改文件名

###### bat\_rename.sh

```shell
#!/bin/sh

### 批量修改文件名
# 文件所在的路径
dir=$1
for file_path in `ls $1`
do
  # 替换文件名
  new_path=$dir${file_path/$2/$3}
  # 修改文件名
  mv $dir$file_path $new_path
  # 输出新文件名
  echo $new_path
  # 替换文件内容
  sed -i "s/$2/$3/g" $new_path
done
```

###### 使用方法 ./bat\_rename.sh 文件所在路径 原文件名 新文件名

```ruby
# 将 test/路径下所有文件名或文件中，包含dev2的字符串，替换为pressure字符串
[tidb@dev10 ~]$ ./bat_rename.sh test/ dev2 pressure
```

* * *

* * *

* * *

###### 6 Shell 批量替换文件内容

```ruby
cat > filter.sh << ERIC
#!/bin/bash

# 批量替换文件内容
for file in \`ls\`
do
  if [[ \$file == *.sql ]]
  then
    sed -i 's/\`CREATED_\` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP/\`CREATED_\` timestamp(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3)/g' \$file
    sed -i 's/\`CREATED_\` timestamp(3) DEFAULT CURRENT_TIMESTAMP/\`CREATED_\` timestamp(3) DEFAULT CURRENT_TIMESTAMP(3)/g' \$file
    echo \$file '已修改!'
  else
    echo '未改变!'
  fi
done
ERIC

```

* * *

* * *

* * *

###### 7 字符串替换

```shell
#!/bin/bash
img="http://www.dev-share.com"
# 将.com字符串替换为.top
echo ${img/.com/.top/}
echo ""
echo -e "\033[32m 完成 \033[0m"

```

* * *

* * *

* * *

##### 8 判断文件是否存在

```shell
#!/bin/bash

## 判断文件是否存在
if [ -f /etc/sudo.conf ]
then
     echo "文件已存在"
else
     echo "文件不存在"
fi

```

```shell
# 判断文件已存在
[root@localhost ~]# test -f /etc/resolv.conf && echo "file exist"
file exist

[root@localhost ~]# test -f /etc/resolv.conf && echo "file exist" || echo "file not exist"
file exist


# 判断文件不存在
[root@localhost ~]# test -f /etc/resolv.conf1 || echo "file not exist"
file not exist

[root@localhost ~]# test -f /etc/resolv.conf1 && echo "file exist" || echo "file not exist"
file not exist


```

[参考链接](https://www.jianshu.com/p/d69895d48124)

* * *

* * *

* * *

##### 9 for循环输出字符串

```shell
cat > show-info.sh < ERIC
for str in openfunction keda dapr-system knative-serving projectcontour shipwright-build tekton-pipelines
do
    printf '%s\n' "$(printf '=%.0s' {1..48}) ${str} $(printf '=%.0s' {1..48})"
    printf 'kubectl -n %s get po\n' $str
    echo
    echo
done

ERIC


## 执行
chmod +x show-info.sh && ./show-info.sh
```

* * *

* * *

* * *
