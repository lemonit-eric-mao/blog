---
title: "Node.js  Puppeteer实现数据采集(一)"
date: "2018-08-30"
categories: 
  - "node-js"
---

```javascript
/**
 * Centos 安装 puppeteer 需要添加以下 依赖库 和 字体
 * # 依赖库
 * yum install pango.x86_64 libXcomposite.x86_64 libXcursor.x86_64 libXdamage.x86_64 libXext.x86_64 libXi.x86_64 libXtst.x86_64 cups-libs.x86_64 libXScrnSaver.x86_64 libXrandr.x86_64 GConf2.x86_64 alsa-lib.x86_64 atk.x86_64 gtk3.x86_64 -y
 * # 字体
 * yum install ipa-gothic-fonts xorg-x11-fonts-100dpi xorg-x11-fonts-75dpi xorg-x11-utils xorg-x11-fonts-cyrillic xorg-x11-fonts-Type1 xorg-x11-fonts-misc -y
 */
const puppeteer = require('puppeteer');

/**
 * puppeteer.launch(opotions)
 * 以下是 opotions 参数说明
 *
 * 参数名称              参数类型              参数说明
 * ignoreHTTPSErrors    boolean             在请求的过程中是否忽略 Https 报错信息，默认为 false
 * headless             boolean             是否以”无头”的模式运行 chrome, 也就是不显示 UI， 默认为 true
 * executablePath       string              可执行文件的路劲，Puppeteer 默认是使用它自带的 chrome webdriver, 如果你想指定一个自己的 webdriver 路径，可以通过这个参数设置
 * slowMo               number              使 Puppeteer 操作减速，单位是毫秒。如果你想看看 Puppeteer 的整个工作过程，这个参数将非常有用。
 * args                 Array(String)       传递给 chrome 实例的其他参数，比如你可以使用”–ash-host-window-bounds=1024x768” 来设置浏览器窗口大小。更多参数参数列表可以参考 https://peter.sh/experiments/chromium-command-line-switches/
 * handleSIGINT         boolean             是否允许通过进程信号控制 chrome 进程，也就是说是否可以使用 CTRL+C 关闭并退出浏览器.
 * timeout              number              等待 Chrome 实例启动的最长时间。默认为30000（30秒）。如果传入 0 的话则不限制时间
 * dumpio               boolean             是否将浏览器进程stdout和stderr导入到process.stdout和process.stderr中。默认为false。
 * userDataDir          string              设置用户数据目录，默认linux 是在 ~/.config 目录，window 默认在 C:\Users{USER}\AppData\Local\Google\Chrome\User Data, 其中 {USER} 代表当前登录的用户名
 * env                  Object              指定对Chromium可见的环境变量。默认为process.env。
 * devtools             boolean             是否为每个选项卡自动打开DevTools面板， 这个选项只有当 headless 设置为 false 的时候有效
 */
(async () => {
    // 启动浏览器实例
    const browser = await puppeteer.launch({headless: false});
    /**
     * Puppeteer 提供了一些 API 供我们修改浏览器终端的配置
     *
     * Page.setViewport()     修改浏览器视窗大小
     * Page.setUserAgent()    设置浏览器的 UserAgent 信息
     * Page.emulateMedia()    更改页面的CSS媒体类型，用于进行模拟媒体仿真。 可选值为 “screen”, “print”, “null”, 如果设置为 null 则表示禁用媒体仿真。
     * Page.emulate()         模拟设备，参数设备对象，比如 iPhone, Mac, Android 等
     */
    const page = await browser.newPage();
    // 改变浏览器窗口大小
    await page.setViewport({width: 1920, height: 1080});

    // 进入百度首页
    await page.goto('https://www.baidu.com');
    // 获取搜索框
    const searchInput = await page.$('#kw');
    // 让光标定位到搜索框
    await searchInput.focus();
    // 模拟人自动填入搜索内容
    await page.keyboard.type('lemonit.cn', {delay: 100});
    // 点击搜索按钮
    await page.click(`#su`);
    // 等待
    await page.waitFor(1000);
    // 截图
    await page.screenshot({path: `baidu-search.png`});

    const resultData = await page.$$eval('#content_left > div > h3 > a', links => {
        return links.map((a) => {
            return {
                href: a.href,
                name: a.text
            }
        });
    });
    console.log(resultData)

    await browser.close();
})();
```
