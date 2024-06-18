---
title: 'docker-compose 安装 wordpress'
date: '2017-11-16T14:47:57+00:00'
status: private
permalink: /2017/11/16/docker-compose-%e5%ae%89%e8%a3%85-wordpress
author: 毛巳煜
excerpt: ''
type: post
id: 412
category:
    - Docker
    - wordpress
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
enclosure:
    - "http://qiniu.dev-share.top/mp3/Alpha-Vangelis.mp3\r\n13777106\r\naudio/mpeg\r\n"
    - "http://qiniu.dev-share.top/mp3/%E5%9C%A8%E8%BD%A9-%E5%B9%BB%E6%98%BC.mp3\r\n3076374\r\naudio/mpeg\r\n"
    - "http://qiniu.dev-share.top/mp3/Tony%20Igy-Astronomia.mp3\r\n2728714\r\naudio/mpeg\r\n"
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
### **[安装 docker-compose](http://www.dev-share.top/2019/06/12/%e5%ae%89%e8%a3%85-docker-compose/ "安装 docker-compose")**

- - - - - -

#### 创建文件夹

```ruby
mkdir -p /home/deploy/wordpress/data
mkdir -p /home/deploy/wordpress/config
cd /home/deploy/wordpress/

```

- - - - - -

#### 添加配置文件，修改wordpress默认配置

```ini
cat > /home/deploy/wordpress/config/uploads.ini 
```

- - - - - -

#### 安装

```ruby
# 创建文件
cat > /home/deploy/wordpress/docker-compose.yml 
```

- - - - - -

#### 启动

```ruby
docker-compose up -d

```

- - - - - -

### 添加定时备份

```ruby
# 下载mydumper
wget http://qiniu.dev-share.top/tidb-mydumper-and-loader.zip

# 创建脚本
cat > /home/deploy/blong_backup.sh 
```

- - - - - -

### **[点击下载主题包](http://qiniu.dev-share.top/wp/hestia.3.0.21.zip "点击下载主题包")**

### **[点击下载 MarkDown工具包](http://qiniu.dev-share.top/wp/WP-Editor.md-10.2.1.zip "点击下载 MarkDown工具包")**

- - - - - -

自定义 音乐播放器
---------

将如下 javascript 加入到 主题 **自定义 --&gt; 小工具 --&gt; 边栏 --&gt; 添加小工具 --&gt; `自定义 html`** 中

```javascript
<div id="mAudioId" style="display: flex;flex-direction: column-reverse;align-items: center;"></div>
<script>

    /**
     * &#24037;&#20855;
     * @param max
     * @returns {number}
     */
    function getRandomInt(max) {
        return Math.floor(Math.random() * Math.floor(max));
    }

    /**
     * &#38899;&#20048;&#21015;&#34920;
     * @type {*[]}
     */
    const audioList = [
        {title: 'Alpha', mp3: 'http://qiniu.dev-share.top/mp3/Alpha-Vangelis.mp3'},
        {title: '&#24187;&#26172;', mp3: 'http://qiniu.dev-share.top/mp3/%E5%9C%A8%E8%BD%A9-%E5%B9%BB%E6%98%BC.mp3'},
        {title: 'TonyIgy-Astronomia', mp3: 'http://qiniu.dev-share.top/mp3/Tony%20Igy-Astronomia.mp3'}
    ];

    function getAudioInfo() {
        return audioList[getRandomInt(audioList.length)];
    }

    /**
     * &#38543;&#26426;&#36873;&#25321;&#27468;&#26354;
     */
    let audioInfo = getAudioInfo();

    /**
     * &#27468;&#26354;&#21517;&#31216;
     */
    let title = document.createElement('span');
    title.innerText = audioInfo.title;

    /**
     * &#38899;&#20048;&#25554;&#20214;
     * @type {HTMLAudioElement}
     */
    let audio = new Audio();
    // &#33258;&#21160;&#25773;&#25918;
    // audio.autoplay = true;
    // &#26174;&#31034;&#38899;&#20048;&#25773;&#25918;&#22120;
    audio.controls = true;
    audio.src = audioInfo.mp3;
    audio.onended = () => {
        audio.src = audioList[getRandomInt(audioList.length)].mp3;
        audio.play();
    }

    /**
     * &#28155;&#21152;&#21040;&#27983;&#35272;&#22120;
     */
    let mAudioId = document.getElementById('mAudioId');
    mAudioId.appendChild(title);
    mAudioId.appendChild(audio);
</script>

```

- - - - - -

自定义 主题额外 CSS样式
--------------

将如下CSS 加入到 主题 **`额外CSS`** 中，可解决主题的样式bug

```css
table th {
    padding: 12px 8px !important;
    text-align: center;
    border:1px solid #ddd;
    background-color:#eff3f5;
}
table td {
    border:1px solid #ddd;
    font-size: 16px;
}

.container {
    width: 80%;
}

p.card-description {
    display: none;
}

div.card-description > p {
    display: none;
}

blockquote {
    padding: 10px 20px;
    margin: 0 0 20px;
    border-left: 5px solid #0f9bf1;
}

blockquote p {
    font-style: normal;
    font-size: 14px;
    font-weight: bold;
}

h1 {
    display: flex;
    justify-content: center;
    font-size: 26px;
}

h2 {
    display: flex;
    font-size: 22px !important;
}

h3 {
    display: flex;
    font-size: 18px !important;
}

h4 {
    display: flex;
    font-size: 16px !important;
}

h5 {
    display: flex;
    font-size: 14px !important;
}

h6 {
    display: flex;
    font-size: 12px !important;
}

.katex {
    font: normal 1.21em KaTeX_Main,Times New Roman,serif;
    display: flex;
    font-size: 16px;
    font-weight: bold;
}

.katex-display {
    display: flex;
    margin: 0;
}

```

- - - - - -

- - - - - -

- - - - - -

**添加微信吸粉插件**
------------

1. **[点击下载插件](http://qiniu.dev-share.top/file/wechat-pilotflow.zip "点击下载插件")**
2. WordPress后台管理端 --&gt; 插件 --&gt; 点击安装插件按钮 --&gt; 点击上传插件
3. 使用如下注释对文章内容进行隐藏

```

                <div style="overflow:hidden; clear:both; width: 100%; height: 40px; position: relative;">
                   <hr style="border:1px dashed #F60;"></hr>
                   <span style="position: absolute;top: 50%;left: 50%; transform: translate(-50%, -50%); background-color: white;">以下为隐藏内容</span>
                </div>
                
在这里的文章的内容会被隐藏


```

- - - - - -

**SEO优化插件**
-----------

**[Smart SEO Tool 点击下载插件](http://qiniu.dev-share.top/file/smart-seo-tool.3.1.2.zip "Smart SEO Tool")**

- - - - - -

- - - - - -

- - - - - -

WordPress 禁用`REST API`和移除`WP-JSON`链接的方法
---------------------------------------

> 将以下代码添加到**主题**`functions.php`文件中即可`禁用REST API`并`移除WP-JSON`链接

```php
/**
 * 禁用REST API、移除wp-json链接
 * 去除head里面输出的链接信息
 */
add_filter('rest_enabled', '_return_false');
add_filter('rest_jsonp_enabled', '_return_false');
remove_action( 'wp_head', 'rest_output_link_wp_head', 10);
remove_action( 'wp_head', 'wp_oembed_add_discovery_links', 10);

/**
 * 禁用未登录用户 REST API
 * 注意： {code: 401, message: "用户没有目标资源的有效身份验证凭据"} 需要使用Linux系统的编码方式，在Windows系统会出现语法错误
 */
add_filter('rest_api_init', 'rest_only_for_authorized_users', 99);
function rest_only_for_authorized_users($wp_rest_server) {
    if(!is_user_logged_in()) {
        wp_die('{code: 401, message: "用户没有目标资源的有效身份验证凭据"}');
    }
}


```

**测试访问：http://www.dev-share.top/wp-json**

- - - - - -

- - - - - -

- - - - - -

### 博客底部备案号`footer.php`

```php
<?php /**
 * The template for displaying the footer
 *
 * Contains the closing of the "wrapper" div and all content after.
 *
 * @package Hestia
 * @since Hestia 1.0
 */
??>
<div style="color: white; background-color: black; height: 100px; display: flex; flex-direction: row-reverse; align-items: center; justify-content: center;">工信部备案号：辽ICP备17016257号-2</div>
<?php wp_footer();??>

```