---
title: 了解JWT
date: '2023-09-01T02:50:48+00:00'
status: private
permalink: /2023/09/01/%e4%ba%86%e8%a7%a3jwt
author: 毛巳煜
excerpt: ''
type: post
id: 10244
category:
    - JWT
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
hestia_layout_select:
    - sidebar-right
---
> JWT（JSON Web Token）是一种用于身份验证和信息传递的开放标准（RFC 7519）。在你的代码中，JWT令牌用于身份验证，以验证用户是否具有访问你的应用程序某些端点的权限。
> 
>  JWT通常由服务器在用户登录成功后生成并返回给客户端。生成JWT令牌通常需要包含一些用户的身份信息，例如用户ID、角色、过期时间等。一般来说，生成JWT的过程包括以下几个步骤：
> 
> 1. 首先要有一个秘钥`"your_secret_key"`, 密钥通常由开发人员自己生成并在应用程序中硬编码。
> 2. 秘钥`"your_secret_key"`是用来生成JWT令牌的。
> 3. 在服务器端，当用户登录成功时，根据用户的身份信息生成JWT令牌。
> 4. 将JWT令牌发送给客户端，通常作为登录成功的响应的一部分。
> 5. 客户端在每次请求受保护的端点时，将JWT令牌包含在请求的Authorization头部中。
> 6. 服务器在接收到请求时，验证JWT令牌的签名和有效期，并根据令牌中包含的信息来判断用户是否有权限访问特定的资源。

- - - - - -

- - - - - -

- - - - - -

JWT 工作原理
========

```bash
 用户登录                     客户端                        服务端
    |                           |                             |
    +-------------------------->|                             |
    |                           |                             |
    |                           |                             |
    |                 +---------------------+                 |
    |                 | 提供凭据(用户名密码) |                |
    |                 +---------------------+                 |
    |                           |                             |
    |                           |                             |
    |                           v                             |
    |                     +-------------+                     |
    |                     | 发送认证请求 |------------------->|
    |                     +-------------+                     |
    |                           |                             |
    |                           |                             |
    |                           |                             |
    |                           |                  +------------------------+
    |                           |                  | 验证凭据，生成 JWT 令牌 |
    |                           |                  +------------------------+
    |                           |                             |
    |                           |                             |
    |                           |                             v
    |                           |                       +--------------+
    |                           |                       | 用户凭据验证 |
    |                           |                       +--------------+
    |                           |                             |
    |                           |                             |
    |                           |                             v
    |                           |                        +----------+
    |                           |                        | 认证成功 |
    |                           |                        +----------+
    |                           |                             |
    |                           |                             |
    |                           |                             v
    |                           |                        +----------+
    |                           |                        | 生成 JWT |
    |                           |                        +----------+
    |                           |                             |
    |                           |                             |
    |                           |                             v
    |                           |                   +---------------------+
    |                           ||
    |                 +---------------------+                 |
    |                           |                             |
    |                           |                             v
    |                           |                        +---------+
    |                           |
```

> 当涉及到在网络通信中安全传递信息时，JSON Web Token（JWT）是一种常见的解决方案。JWT 是一种基于开放标准的、紧凑且自包含的方式，用于在不同实体之间传递信息，例如用户认证、权限控制等。JWT 由三个部分组成：Header（头部）、Payload（有效负荷）和 Signature（签名）。

下面以一个实际的案例来解释 JWT 及其组成部分的作用：

### 案例：用户认证与授权

> 假设我们正在开发一个社交媒体应用，用户需要通过用户名和密码进行登录，并获得访问特定资源的权限。我们将使用 JWT 来处理用户认证和授权。

1. **Header（头部）：**JWT 的头部包含了元数据信息，通常用于指定所使用的签名算法和令牌类型。这是一个使用 Base64 编码的 JSON 对象。例如，我们可以使用如下头部：
  
  ```json
  {
   "alg": "HS256",
   "typ": "JWT"
  }
  
  ```
  
  在这里，`alg` 表示所使用的签名算法（HMAC SHA-256），`typ` 表示令牌类型（JWT）。
2. **Payload（有效负荷）：**
  
  Payload 包含了实际的数据内容，这些数据可以是用户身份信息、权限、声明等。这部分也是一个使用 Base64 编码的 JSON 对象。例如：
  
  ```json
  {
   "sub": "user123",
   "name": "John Doe",
   "role": "user",
   "exp": 1672716000
  }
  
  ```
  
  在这里，`sub` 表示主题（Subject），即用户ID；`name` 表示用户姓名；`role` 表示用户角色；`exp` 表示过期时间（Unix 时间戳），以此来限制令牌的有效性。
3. **Signature（签名）：**
  
  签名用于验证 JWT 的完整性和真实性。它由头部、有效负荷和一个密钥（只有服务器知道）组成，然后通过指定的签名算法进行加密。例如，使用 HMAC SHA-256 算法可以生成签名。

**综合起来，一个完整的 JWT 如下所示：**

```bash
Header（头部）.Payload（有效负荷）.Signature（签名）

```

#### 生成的JWT

```bash
+---------------------+    +-----------------------+    +-------------------+
| Header              | => | Payload               | => | Signature         |
| {                   |    | {                     |    |                   |
|    "alg": "HS256",  |    |  "sub": "user123",    |    |                   |
|    "typ": "JWT"     |    |  "name": "John Doe",  |    |                   |
| }                   |    |  "role": "admin",     |    |                   |
|                     |    |  "exp": 1672716000    |    |                   |
|                     |    | }                     |    |                   |
|                     |    |                       |    |                   |
+---------------------+    +-----------------------+    +-------------------+


```

**在我们的案例中，一个 JWT 可能如下所示：**

```bash
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMTIzIiwibmFtZSI6IkpvaG4gRG9lIiwicm9sZSI6InVzZXIiLCJleHAiOjE2NzI3MTYwMDB9.FiWZqFLn9m6Bj-DaMjZzLZR7YotqIn7dOwJvkmkH2Dc

```

在实际应用中，服务器可以将该 JWT 发送给客户端（例如浏览器），客户端可以将其存储在本地。每当客户端想要访问需要授权的资源时，它会将 JWT 放在请求的头部或其他位置，然后服务器可以验证 JWT 的完整性、真实性和有效性，从而决定是否授予访问权限。

示例
--

使用 Go 语言实现：

```go
package main

import (
    "fmt"
    "time"
    "github.com/dgrijalva/jwt-go"
)

func main() {
    // 定义密钥
    mySigningKey := []byte("mysecretkey")

    // 创建 JWT 的 Header
    tokenHeader := jwt.NewHeader(jwt.SigningMethodHS256)

    // 创建 JWT 的 Payload
    claims := jwt.MapClaims{
        "sub": "user123",
        "name": "John Doe",
        "role": "admin",
        "exp": time.Now().Add(time.Hour * 24).Unix(), // 设置过期时间为 24 小时后
    }

    // 创建 JWT
    token := jwt.NewWithClaims(tokenHeader, claims)

    // 对 JWT 进行签名，生成最终的令牌字符串
    tokenString, err := token.SignedString(mySigningKey)
    if err != nil {
        fmt.Println("Error creating token:", err)
        return
    }

    fmt.Println("JWT Token:", tokenString)
}

```

在这个示例中，我们使用了 `github.com/dgrijalva/jwt-go` 这个 Go 包来操作 JWT。请确保你的 Go 项目中已经引入了该包。