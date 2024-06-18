---
title: "微信小程序-常见问题"
date: "2019-08-07"
categories: 
  - "移动端"
---

###### 分包项目配置说明 **[项目地址](https://gitee.com/eric-mao/applet-example/tree/example/#applet-example "项目地址")**

```json
{
    "pages": [                                   # 主应用程序的路径配置，注意："pages": []中只允许配置主包中的路径
        "packages/pages/home/home",              # 配置首页，如果不明确指定首页，默认第一项就是首页
        "tabBar/component/index",
        "tabBar/API/index",
        "tabBar/weui/index"
    ],
    "subpackages": [                             # 配置子应用程序包
        {
            "root": "subPackages/component",     # 指定子程序component的根目录在哪
            "pages": [                           # 配置子应用程序路径，注意："subpackages": [] --> "pages": [] 中必须要放置所有子应用程序的路径，如果缺少了配置，首次跳转子程序页面会不可达
                "pages/....../......",
                "pages/....../......"
            ]
        },
        {
            "root": "subPackages/API",           # 指定子程序API的根目录在哪
            "pages": [
                "pages/....../......",
                "pages/....../......"
            ]
        },
        {
            "root": "subPackages/weui",          # 指定子程序weui的根目录在哪
            "pages": [
                "pages/....../......",
                "pages/....../......"
            ]
        }
    ],
    "tabBar": {                                  # 配置当前应用程序的tabbar
        "color": "@tabBarColor",
        "selectedColor": "@tabBarSelectedColor",
        "borderStyle": "@tabBarBorderStyle",
        "backgroundColor": "@tabBarBackgroundColor",
        "list": [
            {
                "pagePath": "packages/pages/home/home",               # 注意：此配置中的路径必须是在"pages": []中已经存在的路径
                "iconPath": "@iconPathComponent",
                "selectedIconPath": "@selectedIconPathComponent",
                "text": "应用"
            },
            {
                "pagePath": "tabBar/component/index",                 # 注意：此配置中的路径必须是在"pages": []中已经存在的路径
                "iconPath": "@iconPathComponent",
                "selectedIconPath": "@selectedIconPathComponent",
                "text": "原生组件"
            },
            {
                "pagePath": "tabBar/API/index",                       # 注意：此配置中的路径必须是在"pages": []中已经存在的路径
                "iconPath": "@iconPathAPI",
                "selectedIconPath": "@selectedIconPathAPI",
                "text": "接口"
            },
            {
                "pagePath": "tabBar/weui/index",                      # 注意：此配置中的路径必须是在"pages": []中已经存在的路径 
                "iconPath": "@iconPathComponent",
                "selectedIconPath": "@selectedIconPathComponent",
                "text": "WEUI"
            }
        ]
    },
    "themeLocation": "dhc.theme.json",                                # 引用自定义主题色
    ......
}
```

* * *

* * *

* * *

###### 页面跳转

```javascript
// 保留当前页面，跳转到应用内的某个页面（最多打开5个页面，之后按钮就没有响应的）
wx.navigateTo({
    url: "/pages/aaa/aaa"
})

// 关闭当前页面，跳转到应用内的某个页面（这个跳转有个坑，就是跳转页面后页面会闪烁一下。）
wx.redirectTo({
    url: "/pages/aaa/aaa"
})

// 跳转至指定页面并关闭其他打开的所有页面（这个最好用在返回至首页的的时候）
wx.reLaunch({

    url: '/pages/index/index'

})

// 跳转到tabBar页面，并关闭其他所有tabBar页面
wx.switchTab({
    url: "/pages/aaa/aaa"
})

// 返回上一页面或多级页面
wx.navigateBack({
    delta: 1
})

// 跳转到tabBar页面(首页), 并刷新
wx.switchTab({
    url: '/pages/home-page/home',
    success() {
        let page = getCurrentPages().pop();
        if (!page) return;
        page.onLoad();
    }
});
```
