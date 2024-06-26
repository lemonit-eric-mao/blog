---
title: "HTTP/1.1 通用首部字段 Cache-Control"
date: "2017-11-16"
categories: 
  - "网络基础"
---

## **Cache-Control**

### **缓存请求指令**

**no-cache** `无` 强制向源服务器再次验证 **no-store** `无` 不缓存请求或响应的任何内容 **max-age= \[ 秒\]** `必需` 响应的最大Age值 **max-stale( = \[ 秒\])** `可省略` 接收已过期的响应 **min-fresh= \[ 秒\]** `必需` 期望在指定时间内的响应仍有效 **no-transform** `无` 代理不可更改媒体类型 **only-if-cached** `无` 从缓存获取资源 **cache-extension** `-` 新指令标记(token)

### **缓存响应指令**

**public** `无` 可向任意方提供响应的缓存 **private** `可省略` 仅向特定用户返回响应 **no-cache** `可省略` 缓存前必须先确认其有效性 **no-store** `无` 不缓存请求或响应的任何内容 **no-transform** `无` 代理不可更改媒体类型 **must-revalidate** `无` 可缓存但必须再向源服务器进行确认 **proxy-revalidate** `无` 要求中间缓存服务器对缓存的响应有效性再进行确认 **max-age = \[ 秒\]** `必需` 响应的最大Age值 **s-maxage = \[ 秒\]** `必需` 公共缓存服务器响应的最大Age值 **cache-extension** `-` 新指令标记(token)

### **注意事项**

从字面意思上很容易把 no-cache `误解成为不缓存`, 但事实上 no-cache 代表`不缓存过期的资源`, 缓存会向源服务器进行有效期确认后处理资源, no-store 才是`真正地不进行缓存`,请读者注意区别理解。
