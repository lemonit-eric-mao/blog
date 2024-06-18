---
title: "什么是跨域、同源策略？"
date: "2017-11-16"
categories: 
  - "前端开发"
---

## **跨域**

   **跨域**，指的是浏览器不能执行其他网站的脚本。它是由浏览器的同源策略造成的，是浏览器对JavaScript施加的安全限制。

* * *

### **同源([官方说明](https://developer.mozilla.org/zh-CN/docs/Web/Security/Same-origin_policy "官方说明"))**

### **`同源的定义`**

   浏览器同源的定义，如果两个 URL 的 protocol、port (如果有指定的话)和 host 都相同的话，则这两个 URL 是同源。

确定同源的方法： URL的 **`协议`/`主机`/`端口`相同, `与路径无关`**

**下表给出了与 URL `http://store.company.com/dir/page.html` 的源进行对比的示例:**

| **URL** | **结果** | **原因** |
| --- | :-: | --- |
| http://store.company.com/dir2/other.html | **同源** | 只有路径不同 |
| http://store.company.com/dir/inner/another.html | **同源** | 只有路径不同 |
| https://store.company.com/secure.html | `失败` | 协议不同 |
| http://store.company.com:81/dir/etc.html | `失败` | 端口不同 ( http:// 默认端口是80) |
| http://news.company.com/dir/other.html | `失败` | 主机不同 |

* * *

* * *

* * *
