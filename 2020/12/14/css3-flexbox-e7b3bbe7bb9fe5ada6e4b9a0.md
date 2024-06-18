---
title: 'CSS3 FlexBox 系统学习'
date: '2020-12-14T05:59:50+00:00'
status: publish
permalink: /2020/12/14/css3-flexbox-%e7%b3%bb%e7%bb%9f%e5%ad%a6%e4%b9%a0
author: 毛巳煜
excerpt: ''
type: post
id: 6632
category:
    - CSS
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### **思路** 就像盖楼一样

1. 先买块儿地(`定位`)
2. 打地基(`设置基础空间大小`)
3. 在屋内添加隔断(`布局`)
4. 在一层一层的向上添砖加瓦(`添加子层`)
5. 在室外装修(`美化样式、添加动画效果`)

- - - - - -

###### 1 先买块儿地(`定位`)

```
<pre data-language="HTML">```markup


<div class="dl-foundation">
</div>


```
```

- - - - - -

###### 2 打地基(`设置基础空间大小`)

```
<pre data-language="HTML">```markup


<div class="dl-foundation">
    <div class="dl-wrapper">
    </div>
</div>


```
```

- - - - - -

###### 3 在屋内添加隔断(`布局`)

```
<pre data-language="HTML">```markup


<div class="dl-foundation">
    <div class="dl-wrapper">
        
        <div class="dl-mask">
            
            <div class="dl-dialog" onclick="recovery(this)">
                
                <div class="dl-title">
                </div>
                
                <div class="dl-content"></div>
                
                <div class="dl-buttons">
                </div>
            </div>
        </div>
    </div>
</div>


```
```

- - - - - -

###### 4 在一层一层的向上发展(`添加子层`)

```
<pre data-language="HTML">```markup


<div class="dl-foundation">
    <div class="dl-wrapper">
        
        <div class="dl-mask">
            
            <div class="dl-dialog" onclick="recovery(this)">
                
                <div class="dl-title">
                    <div class="dl-text">标题栏</div>
                    <div>
                        
                        <svg class="icon" height="20px" onclick="minimize(this)" version="1.1" viewbox="0 0 1024 1024" width="20px" xmlns="http://www.w3.org/2000/svg">
                            <path d="M76.8 563.2h819.2a51.2 51.2 0 0 0 0-102.4h-819.2a51.2 51.2 0 0 0 0 102.4z" fill="#333333"></path>
                        </svg>
                    </div>
                </div>
                
                <div class="dl-content">正文</div>
                
                <div class="dl-buttons">
                    <div>关闭</div>
                    <div>确定</div>
                </div>
            </div>
        </div>
    </div>
</div>


```
```

- - - - - -

- - - - - -

- - - - - -

###### 5 在室外装修(`美化样式、添加动画效果`) **`完整代码`**

```css



    <meta charset="UTF-8"></meta>
    <title></title>

    
    <style>
        @keyframes minimize {
            /*&#20174;&#24403;&#21069;&#27491;&#24120;&#30340;&#27604;&#20363;*/
            from {
                transform: scale(1, 1);
            }
            /*&#32553;&#25918;&#21040;&#24403;&#21069;&#27604;&#20363;&#30340;1%*/
            to {
                /*transform&#23646;&#24615;&#23427;&#20204;&#30340;&#25191;&#34892;&#39034;&#24207;&#26159;&#20174;&#21518;&#21521;&#21069;&#25191;&#34892;&#30340;&#65292; &#20808;&#25191;&#34892;scale&#65292; &#22312;&#25191;&#34892; translate*/
                transform: translate(-55%, 55%) scale(0.1, 0.1);
            }
        }

        @keyframes recovery {
            /*&#20174;&#24403;&#21069;&#32553;&#25918;&#30340;&#27604;&#20363;*/
            from {
                transform: translate(-55%, 55%) scale(0.1, 0.1);
            }
            /*&#24674;&#22797;&#21040;&#27491;&#24120;&#30340;&#27604;&#20363;*/
            to {
                transform: scale(1, 1);
            }
        }
    </style>

    
    <style>
        html, body {
            padding: 0;
            margin: 0;
            border: 0;
        }

        /*&#22320;&#22522;*/
        .dl-foundation {
            /*&#22266;&#23450;&#23450;&#20301;*/
            position: fixed;
            top: 0;
            left: 0;
            /*&#26631;&#35782;&#32972;&#26223;&#36879;&#26126;&#65292;&#24182;&#19988;&#19981;&#24433;&#21709;&#23376;&#23618;&#30340;&#36879;&#26126;&#24230;*/
            background: rgba(0, 0, 0, 0);
            /*&#26631;&#35782;&#20803;&#32032;&#27809;&#26377;&#40736;&#26631;&#20107;&#20214;&#65292;&#24182;&#19988;&#20107;&#20214;&#21487;&#20197;&#31359;&#36879;*/
            pointer-events: none;
            /*&#20805;&#28385;&#23631;&#24149;*/
            width: 100vw;
            height: 100vh;
            /*&#20351;&#29992;flexbox&#24067;&#23616;&#65292;&#35201;&#24819;&#20351;&#29992;flexbox&#27599;&#19968;&#23618;&#37117;&#24471;&#20889;display: flex;&#65292;&#23376;&#23618;&#19981;&#20250;&#32487;&#25215;&#29238;&#23618;&#30340;flexbox*/
            display: flex;
        }

        .dl-foundation > .dl-wrapper {
            /*&#26631;&#35782;&#32972;&#26223;&#36879;&#26126;&#65292;&#24182;&#19988;&#19981;&#24433;&#21709;&#23376;&#23618;&#30340;&#36879;&#26126;&#24230;*/
            background: rgba(0, 0, 0, 0);
            /*&#34920;&#31034;&#23376;&#23618;&#30340;&#31354;&#38388;&#21344;&#27604;&#65292; &#29238;&#23618;&#24517;&#39035;&#26159;flexbox&#25165;&#36215;&#20316;&#29992;*/
            flex: 1;
            display: flex;
        }

        /*&#36974;&#32617;*/
        .dl-foundation > .dl-wrapper > .dl-mask {
            background: rgba(189, 189, 189, 0.5);
            flex: 1;
            display: flex;
            /*&#35753;&#23376;&#23618;&#27700;&#24179;&#22402;&#30452;&#23621;&#20013;*/
            justify-content: center;
            align-items: center;
        }

        /*&#23545;&#35805;&#26694;*/
        .dl-foundation > .dl-wrapper > .dl-mask > .dl-dialog {
            /*&#38452;&#24433;*/
            /*
             * box-shadow: x&#36724;&#20559;&#31227;&#37327;&#20801;&#35768;&#36127;&#20540;   y&#36724;&#20559;&#31227;&#37327;&#20801;&#35768;&#36127;&#20540;   &#38452;&#24433;&#30340;&#27169;&#31946;&#36317;&#31163;   &#38452;&#24433;&#30340;&#23610;&#23544;   #1e90ff70;
             * box-shadow:              1px                                   1px                               10px                     10px       #1e90ff70;
            */
            box-shadow: 1px 1px 10px 10px #1e90ff70;
            /*&#24403;&#21069;&#23618;&#22823;&#23567;*/
            width: 80vw;
            height: 80vh;
            /*&#26631;&#35782;&#24674;&#22797;&#20803;&#32032;&#40736;&#26631;&#20107;&#20214;*/
            pointer-events: auto;
            background-color: #FFF;
            display: flex;
            /**
             * &#35753;&#23376;&#23618;&#22402;&#30452;&#26174;&#31034;
             *     row                                 &#40664;&#35748;&#20540;&#12290;&#28789;&#27963;&#30340;&#39033;&#30446;&#23558;&#27700;&#24179;&#26174;&#31034;&#65292;&#27491;&#22914;&#19968;&#20010;&#34892;&#19968;&#26679;
             *     row-reverse                &#19982; row &#30456;&#21516;&#65292;&#20294;&#26159;&#20197;&#30456;&#21453;&#30340;&#39034;&#24207;
             *     column                         &#28789;&#27963;&#30340;&#39033;&#30446;&#23558;&#22402;&#30452;&#26174;&#31034;&#65292;&#27491;&#22914;&#19968;&#20010;&#21015;&#19968;&#26679;
             *     column-reverse        &#19982; column &#30456;&#21516;&#65292;&#20294;&#26159;&#20197;&#30456;&#21453;&#30340;&#39034;&#24207;
             */
            flex-direction: column;
            /**
             * stretch&#65306; &#26631;&#35782;&#23376;&#23618;&#20840;&#26159;100%
             * center&#65306; &#26631;&#35782;&#23376;&#23618;&#29992;&#22810;&#23569;&#21344;&#22810;&#23569;&#24182;&#19988;&#23621;&#20013;
             */
            align-items: stretch;
        }

        /*&#23545;&#35805;&#26694; &#26368;&#23567;&#21270;*/
        .dl-foundation > .dl-wrapper > .dl-mask > .dl-dialog-minimize {
            animation: minimize 1s;
            /*transform&#23646;&#24615;&#23427;&#20204;&#30340;&#25191;&#34892;&#39034;&#24207;&#26159;&#20174;&#21518;&#21521;&#21069;&#25191;&#34892;&#30340;&#65292; &#20808;&#25191;&#34892;scale&#65292; &#22312;&#25191;&#34892; translate*/
            transform: translate(-55%, 55%) scale(0.1, 0.1);
        }

        /*&#23545;&#35805;&#26694; &#22797;&#21407;*/
        .dl-foundation > .dl-wrapper > .dl-mask > .dl-dialog-recovery {
            animation: recovery 1s;
            transform: scale(1, 1);
        }

        /*&#26631;&#39064;&#26639;*/
        .dl-foundation > .dl-wrapper > .dl-mask > .dl-dialog > .dl-title {
            background-color: #26b58f;
            display: flex;
            /**
             * space-between: &#26631;&#35782;&#23376;&#23618;&#20004;&#31471;&#23545;&#40784;
             */
            justify-content: space-between;
        }

        /*&#26631;&#39064;&#26639;&#25991;&#23383;*/
        .dl-foundation > .dl-wrapper > .dl-mask > .dl-dialog > .dl-title > .dl-text {
        }

        /*&#27491;&#25991;*/
        .dl-foundation > .dl-wrapper > .dl-mask > .dl-dialog > .dl-content {
            background-color: green;
            flex: 1;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /*&#25353;&#38062;*/
        .dl-foundation > .dl-wrapper > .dl-mask > .dl-dialog > .dl-buttons {
            background-color: #0077c5;
            display: flex;
            /**
             * space-around: &#26631;&#35782;&#23376;&#23618;&#20808;&#24179;&#20998;&#65292;&#21518;&#23621;&#20013;
             */
            justify-content: space-around;
            align-items: center;
        }
    </style>


<input onclick="alert('测试鼠标事件穿透')" type="button" value="测试弹窗"></input>

<div class="dl-foundation">
    <div class="dl-wrapper">
        
        <div class="dl-mask">
            
            <div class="dl-dialog" onclick="recovery(this)">
                
                <div class="dl-title">
                    <div class="dl-text">标题栏</div>
                    <div>
                        
                        <svg class="icon" height="20px" onclick="minimize(this)" version="1.1" viewbox="0 0 1024 1024" width="20px" xmlns="http://www.w3.org/2000/svg">
                            <path d="M76.8 563.2h819.2a51.2 51.2 0 0 0 0-102.4h-819.2a51.2 51.2 0 0 0 0 102.4z" fill="#333333"></path>
                        </svg>
                    </div>
                </div>
                
                <div class="dl-content">正文</div>
                
                <div class="dl-buttons">
                    <div>关闭</div>
                    <div>确定</div>
                </div>
            </div>
        </div>
    </div>
</div>

<script>
    /**
     * &#26368;&#23567;&#21270;
     * @param obj
     */
    function minimize(obj) {

        this.event.stopPropagation();

        // &#29238;&#23618;
        let parent = obj.parentElement.parentElement.parentElement;

        parent.classList.remove('dl-dialog-recovery');
        parent.classList.add('dl-dialog-minimize');
    }

    /**
     * &#22797;&#21407;
     * @param obj
     */
    function recovery(obj) {

        // &#21028;&#26029;&#65292;&#22914;&#26524;&#24403;&#21069;&#29366;&#24577;&#19981;&#26159;&#26368;&#23567;&#21270;&#65292;&#30452;&#25509;&#36820;&#22238;
        if (!obj.classList.contains('dl-dialog-minimize')) {
            return;
        }

        obj.classList.remove('dl-dialog-minimize');
        obj.classList.add('dl-dialog-recovery');
    }
</script>


```