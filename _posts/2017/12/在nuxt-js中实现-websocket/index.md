---
title: "在nuxt.js中实现 webSocket"
date: "2017-12-21"
categories: 
  - "vue"
---

##### 在nuxt.js中实现 webSocket

##### web-socket.js

```javascript
/**
 * 封装 添加断线重连
 * Created by mao-siyu on 17-12-21.
 */
class WS {

  constructor(success) {
    this.intervalId;
    this.main();
    this.success = success;
  }

  connect() {
    // this.webSocket = new WebSocket(`ws://${this.url}`);
    this.webSocket = new WebSocket(`ws://10.32.159.216:8080/smartcity/statistical/websocket`);
  }

  onopen() {
    this.webSocket.onopen = (evt) => {
      console.log('%c%s', 'color:purple;', '=============服务器已连接=============');
      if (this.intervalId) {
        window.clearInterval(this.intervalId);
        this.intervalId = null;
      }
      this.success(this);
    }
  }

  onclose() {
    this.webSocket.onclose = (evt) => {
      console.log('%c%s', 'color:blue;', '=============网络连接已断开=============');
      if (!this.intervalId) {
        this.intervalId = setInterval(() => {
          console.log('%c%s', 'color:blue;', '=============正在尝试重新连接=============');
          this.main();
        }, 2000);
      }
    }
  }

  onerror() {
    this.webSocket.onerror = (evt) => {
      console.log('%c%s', 'color:red;', '=============连接异常=============');
    };
  }

  onmessage(callback) {
    this.webSocket.onmessage = (evt) => {
      // console.log('%c%s', 'color:green;', evt.data);
      callback(evt.data);
    }
  }

  send(info) {
    this.webSocket.send(info);
  }

  main() {
    this.connect();
    this.onopen();
    this.onclose();
    this.onerror();
  }

}

export default WS;
```

##### 在vue文件中使用

##### web-socket.vue

```javascript
import WebSocket from '~/plugins/web-socket'

const initWS = () => {
  new WebSocket((ws) => {
    ws.onmessage((data) => {
      console.log('%c%s', 'color:green;', data);
    });
  });
}

export default {
    mounted() {
        initWS(this);
    },
    methods: {},
}
```

* * *

* * *

* * *

##### node.js Websocket 服务端 测试

```javascript
/**
 * Created by mao-siyu on 17-12-21.
 */
const nws = require('nodejs-websocket');

let intervalId = null;

const nwsServer = nws.createServer(function (connect) {

    /**
     * 消息
     */
    connect.on('text', function (txt) {
        console.log('onText =:|======> : ' + txt);
    });

    /**
     * 某次的连接是否关闭
     */
    connect.on('close', function (code) {
        console.info('onClose =:|======> code: ' + code);
        clearInterval(intervalId);
    });

    connect.on('error', function (code, reason) {
        console.error('onError =:|======> code: ' + code + ' reason: ' + reason);
    });

});

/**
 * websocket 服务监听 已经启动
 */
nwsServer.on('listening', function () {
    console.log('nws.js onListening =:|======>  初始化 nws');
});

/**
 * websocket 客户端链接事件
 */
nwsServer.on('connection', function (connect) {
    console.log('nws.js onConnection =:|======> Your connection key is: ' + connect.key);
    connect.send('Your connection key is: ' + connect.key);
    intervalId = setInterval(() => {
        connect.send('你好我是 Server' + new Date());
    }, 1000);
});

nwsServer.listen(10086);

module.exports = nwsServer;

```

* * *

* * *

* * *

##### spring-boot 服务端 测试

##### MyWebSocket.java

```java
package org.framework.smartcity.bigdata.statistical.controller;

import com.google.gson.Gson;
import org.framework.smartcity.bigdata.statistical.common.aop.DataSourceAop;
import org.framework.smartcity.bigdata.statistical.entity.MyWebSocketProtocol;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import javax.websocket.*;
import javax.websocket.server.ServerEndpoint;
import java.io.IOException;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * webSocket
 *
 * @author mao_siyu
 */
@ServerEndpoint(value = "/websocket")
@Component
public class MyWebSocket {

    private static Logger logger = LoggerFactory.getLogger(DataSourceAop.class);

    private final static Gson gson = new Gson();

    private final static Map<String, Session> MY_WEBSOCKET_SESSION = new ConcurrentHashMap<>();

    /**
     * 连接建立成功调用的方法
     */
    @OnOpen
    public void onOpen(Session session) {
        logger.info("已连接----------");
        MY_WEBSOCKET_SESSION.put(session.getId(), session);
    }

    /**
     * 收到客户端消息后调用的方法
     *
     * @param message 客户端发送过来的消息
     */
    @OnMessage
    public void onMessage(String message, Session session) throws IOException {
        logger.info("来自客户端的消息:" + message);
    }

    /**
     * 连接关闭调用的方法
     */
    @OnClose
    public void onClose(Session session) {
        logger.info("关闭");
        MY_WEBSOCKET_SESSION.remove(session.getId());
    }

    /**
     * 发生错误时调用
     */
    @OnError
    public void onError(Session session, Throwable error) {
        logger.error("发生错误");
        MY_WEBSOCKET_SESSION.remove(session.getId());
    }

    /**
     * 群发自定义消息
     */
    public static void sendInfo(MyWebSocketProtocol wsp) throws IOException {
        // wsp.getHead().put("", "");
        // wsp.getBody().put("", "");
        MY_WEBSOCKET_SESSION.forEach((k, v) -> {
            try {
                v.getBasicRemote().sendText(gson.toJson(wsp));
            } catch (IOException e) {
                e.printStackTrace();
            }
        });
    }
}
```

##### 自定义webSocket请求协议

###### MyWebSocketProtocol.java

```java
package org.framework.smartcity.bigdata.statistical.entity;

import java.util.HashMap;
import java.util.Map;

/**
 * WebSocket 请求协议
 * 注意 这个类的属性只提供get方法，请不要开启set方法!
 * @author mao_siyu
 */
public class MyWebSocketProtocol {

    private Map<String, String> head;
    private Map<String, Object> body;

    public MyWebSocketProtocol() {
        head = new HashMap<>();
        body = new HashMap<>();
    }

    public Map<String, String> getHead() {
        return head;
    }

    public Map<String, Object> getBody() {
        return body;
    }
}
```

##### java服务端推送写法

```java
    private static void main(String[] args) {
    MyWebSocketProtocol wsp = new MyWebSocketProtocol();
    wsp.getHead().put("state", "部件的实时推送！");
    wsp.getBody().put("data", "实体数据！");
    // 推送信息
    MyWebSocket.sendInfo(wsp);
}
```
