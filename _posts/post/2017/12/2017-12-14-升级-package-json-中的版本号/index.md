---
title: "升级 package.json 中的版本号"
date: "2017-12-14"
categories: 
  - "node-js"
---

##### 版本号的含义

**如: 1.0.6**

- 第1位: 表示版本升级
- 第2位: 表示特性更新
- 第3位: 表示修订补丁

**示例：**

- 版本升级: 2.0.6
- 特性更新: 1.1.6
- 修订补丁: 1.0.7

* * *

##### 安装 npm-check

```ruby
mao-siyu@mao-siyu-PC:~/文档/code/dist-server$ sudo npm i -g npm-check
npm notice created a lockfile as package-lock.json. You should commit this file.
+ npm-check@5.6.0
added 240 packages in 27.361s
mao-siyu@mao-siyu-PC:~/文档/code/dist-server$
```

* * *

##### sudo npm-check 检查对应的版本信息

```ruby
mao-siyu@mao-siyu-PC:~/文档/code/dist-server$ sudo npm-check

body-parser   😎  MINOR UP  Minor update available. https://github.com/expressjs/body-parser#readme
                           npm install --save body-parser@1.18.2 to go from 1.15.2 to 1.18.2

debug         😎  MAJOR UP  Major update available. https://github.com/visionmedia/debug#readme
                           npm install --save debug@3.1.0 to go from 2.2.0 to 3.1.0
              😕  NOTUSED?  Still using debug?
                           Depcheck did not find code similar to require('debug') or import from 'debug'.
                           Check your code before removing as depcheck isn't able to foresee all ways dependencies can be used.
                           Use --skip-unused to skip this check.
                           To remove this package: npm uninstall --save debug

morgan        😎  MINOR UP  Minor update available. https://github.com/expressjs/morgan#readme
                           npm install --save morgan@1.9.0 to go from 1.7.0 to 1.9.0

Use npm-check -u for interactive update.
mao-siyu@mao-siyu-PC:~/文档/code/dist-server$
```

* * *

##### sudo npm-check -u 手动选择要升级的模块

```ruby
mao-siyu@mao-siyu-PC:~/文档/code/dist-server$ sudo npm-check -u
? Choose which packages to update. (Press <space> to select)

 Minor Update New backwards-compatible features.
❯◯ body-parser  1.15.2  ❯  1.18.2  https://github.com/expressjs/body-parser#readme
 ◯ morgan       1.7.0   ❯  1.9.0   https://github.com/expressjs/morgan#readme

 Major Update Potentially breaking API changes. Use caution.
 ◯ debug missing  2.2.0  ❯  3.1.0  https://github.com/visionmedia/debug#readme

 Space to select. Enter to start upgrading. Control-C to cancel.
```
