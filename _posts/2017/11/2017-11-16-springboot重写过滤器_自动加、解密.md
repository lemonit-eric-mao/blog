---
title: "SpringBoot重写过滤器_自动加、解密"
date: "2017-11-16"
categories: 
  - "spring-boot"
---

#### 应用环境

SpringBoot v1.4.2

#### 业务需求

```null
  客户端以 RC4 密文的方式向springBoot实现的服务端提交请求密文（原有明文的格式都必须是json格式）,
  服务端在不改动任何原有的Controller实现方式,对密文进行解密并且不影响数据对象的映射(要主是对象数据中还包含其它的集合对象);
```

#### 客户端请求代码

```javascript
    // PUT 请求方式 明文数据
    var data = {
        uno: "09876543",
        uname: "土豪",
        createuser: "yantuhao",
        userList: [{
            uno: "12389756",
            uname: "张三",
            createuser: "李四"
        }]
    };

    $.ajax({
        cache: false,
        async: true,
        contentType: "application/json",
        // 密文数据 加密的方式这里不做讲解,网上案例很多
        data: 'data=2e7bc210e5c9eae9b25f25e642d8afe13929810902b0d2c84bd8ce9205bad53078f38f8a62c76f091d2b17445ab07054c51c89bd367f0418ee87d96cab5e43105d06198fc3ead3cefaa31ce589a3706a32ce9db885ea1928b866a5164aed07c06237e222ec33ace1e178bacbfc83ce553cd2b8f8d2730d10f521bd385aeb47d8fc40',
        type: 'PUT',
        dataType: 'json',
        url: 'http://10.32.156.88:9091/api/user/update/123',
        success: function (result) {
        },
        error: function (xhr, status, error) {
        }
    });
```

这段代码注意看客户端数据传输格式 contentType: "application/json", 而SpringBoot 的PUT过滤器目前只支持解析application/x-www-form-urlencoded格式数据。 在看Controller代码

```java
/**
 * @Author Reverb
 * @Date 2016-11-18 13:07
 * @DESCRIPTION:
 */
@RestController
@RequestMapping("/user")
public class UserController extends CommonController {

    private Gson gson = new Gson();

    @Autowired
    private DlfcUserService dlfcUserService;

    @ResponseBody
    @RequestMapping(value = "/insert", method = RequestMethod.POST)
    public DlfcUser insert(@RequestBody DlfcUser user) throws Exception {

        return user;
    }

    @ResponseBody
    @RequestMapping(value = "/delete/{uid}", method = RequestMethod.DELETE)
    public String deleteByPrimaryKey(@PathVariable("uid") String uid) {

        return uid;
    }

    @ResponseBody
    @RequestMapping(value = "/update/{uid}", method = RequestMethod.PUT)
    public String updateAllByPrimaryKey(@PathVariable("uid") String id, @RequestBody DlfcUser data) {

        return "success";
    }

    @ResponseBody
    @RequestMapping(value = "/select", method = RequestMethod.GET)
    public String selectList(String uid) {

        DlfcUser dlfcUser = dlfcUserService.selectDlfcUserById(uid);
        return DlfcCommonResponse.getInstance().build(dlfcUser);
    }
}
```

接收PUT请求的方法 与 POST的方法是不是很相似? 接下来讲解为什么这么实现。 **先说入的坑:::::比较痛苦的地方**

```null
PUT过滤器 能处理的数据格式是  a=1111&b=2222&c=3333   但是我们传入的数据是 json {a:"1111", b:"2222", c:"3333"}
所以我尝试对数据格式做了数据转换, 重写了PUT过滤器 通过 request.getInputStream() 来进行获取 然后重写Wrapper 在进行转换,然后在把数据放回去,嘿嘿到这里
确实单个对象可以使用了, 但问题来了,  我们常见的数据格式就是 json中 还有 json数组 例如: json {a:"1111", b:"2222", c:"3333", userList:[{e:"666", g:"444", d:"888"}]}
悲哀了, 这种数据格式要怎么处理成 a=1111&b=2222&c=3333& 后面的......不知道了,找了一天 说>实话 技术有限这个格式是啥真不知道,如果知道 也就直接解决问题了。
```

**出坑吧,时间浪费太多了!换个思路**

```null
既然 Spring Boot 对 POST请求的 JSON数据能解析那么使用POST过滤器 就能解决 这个问题了, 注POST请求过滤器 支持Content-Type: application/json ,也就是说使用了这种
类型就不会在走PUT过滤器了.
```

#### 重写过滤器 doFilterInternal方法

```java
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;
import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.*;

/**
 * RC4 过滤器
 *
 * @author reverb
 */
@Component
public class RC4Filter extends OncePerRequestFilter {

    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {
        // 这里是关键 做数据解密的地方
        RC4RequestWrapper rc4Request = new RC4RequestWrapper(request);
        filterChain.doFilter(rc4Request, response);
    }
}
```

#### 重写HttpServletRequestWrapper实现数据解密

```java
import com.housecenter.common.utils.RC4;
import javax.servlet.ReadListener;
import javax.servlet.ServletInputStream;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletRequestWrapper;
import java.io.BufferedReader;
import java.io.ByteArrayInputStream;
import java.io.IOException;
import java.io.InputStreamReader;

/**
 * Created by mao-siyu on 16-12-1.
 */
public class RC4RequestWrapper extends HttpServletRequestWrapper {

    private HttpServletRequest request;

    /**
     * Constructs a request object wrapping the given request.
     *
     * @param request The request to wrap
     * @throws IllegalArgumentException if the request is null
     */
    public RC4RequestWrapper(HttpServletRequest request) {
        super(request);
        this.request = request;
    }

    /**
     * 主要是重写 getInputStream 方法然后在放回去
     *
     * @return
     * @throws IOException
     */
    @Override
    public ServletInputStream getInputStream() throws IOException {

        BufferedReader reader = new BufferedReader(new InputStreamReader(request.getInputStream()));
        String src;
        while (null != (src = reader.readLine())) {
            // data 是json 数据的key js中写好的数据格式,后面是密文
            if (src.startsWith("data")) {
                src = RC4.decryRC4(src.split("=")[1], "666");
                break;
            }
        }
        // 字符串转成流
        ByteArrayInputStream bais = new ByteArrayInputStream(src.getBytes());

        return new ServletInputStream() {
            @Override
            public int read() throws IOException {
                return bais.read();
            }

            @Override
            public boolean isFinished() {
                return false;
            }

            @Override
            public boolean isReady() {
                return false;
            }

            @Override
            public void setReadListener(ReadListener listener) {

            }
        };
    }
}
```

这种实现方式思路简单了, 只要把json数据解密就可以了, 然后 剩下的事儿就交给 spring boot post 过滤器自己处理

到这里 自动解密功能已经实现，接下来还要实现自动加密的处理。

初衷还是一样,不改变原有的 controller 配置 只在过滤器中处理 之前拦截了request, 那么相对的这次肯定是要对response 进行拦截

#### 在原有的过滤器上拦截response

```java
package com.housecenter.common.filter;

import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;
import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * RC4 过滤器
 *
 * @author reverb
 */
@Component
public class RC4Filter extends OncePerRequestFilter {

    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {

        response.setCharacterEncoding("UTF-8");

        // 拦截request
        RC4RequestWrapper rc4Request = new RC4RequestWrapper(request);
        // 拦截response
        RC4ResponseWrapper rceResponse = new RC4ResponseWrapper(response);

        filterChain.doFilter(rc4Request, rceResponse);
    }
}
```

#### RC4ResponseWrapper类 代码如下 重写HttpServletResponseWrapper

```java
package com.housecenter.common.filter;

import com.housecenter.common.utils.RC4;
import javax.servlet.ServletOutputStream;
import javax.servlet.WriteListener;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpServletResponseWrapper;
import java.io.IOException;

/**
 * Created by mao-siyu on 16-12-1.
 */
public class RC4ResponseWrapper extends HttpServletResponseWrapper {

    /**
     * 存入输出流 unicode码
     */
    private StringBuffer sbuffer = new StringBuffer();

    /**
     * Constructs a response adaptor wrapping the given response.
     *
     * @param response The response to be wrapped
     * @throws IllegalArgumentException if the response is null
     */
    public RC4ResponseWrapper(HttpServletResponse response) {
        super(response);
    }

    /**
     * 截获输出流
     *
     * @return
     * @throws IOException
     */
    @Override
    public ServletOutputStream getOutputStream() throws IOException {

        // 新建一个输出流用来截获输出数据
        ServletOutputStream newSos = new ServletOutputStream() {
            @Override
            public void write(int b) throws IOException {
                sbuffer.append((char) b);
            }

            @Override
            public boolean isReady() {
                return false;
            }

            @Override
            public void setWriteListener(WriteListener listener) {
            }
        };

        // 如果已经截获了数据
        if (sbuffer.length() > 0) {
            // 使用原有的旧的输出流做输出数据 响应
            ServletOutputStream oldSos = super.getOutputStream();
            String resultData = sbuffer.toString();
            resultData = RC4.encryRC4String(resultData, "666");
            // 设定加密后的数据长度（如果不重新指定长度，数据会被自动截断）
            super.setContentLength(resultData.length());
            oldSos.print(resultData);
            oldSos.flush();
            oldSos.close();
        }

        // 注: 这里也是新的输出流, 这个流是不能向客户端输出数据的,
        // 因为它已经不是之前的输出流了,
        // 要想输出数据必须使用之前的输出流实现.
        return newSos;
    }

}
```
