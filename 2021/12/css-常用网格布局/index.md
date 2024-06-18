---
title: "CSS 常用网格布局"
date: "2021-12-02"
categories: 
  - "css"
---

###### 九宫格

```markup
<!-- css flex布局实现响应式九宫格以及calc()计算表达式的值 -->
<!DOCTYPE html>
<html>
<style>
.block-div{
    width: 100%;
    display:flex;
    flex-wrap: wrap;
}
.block-div .block{
    background-color: white;
    border-radius: 2px;
    border:1px  solid #000;
    /* 9宫格 自适应 start */
    width: calc(calc(100% / 3) - 12px);
    margin: 5px;
    height: 50px;
    /* 9宫格 自适应 end */
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}
</style>
<body>
   <div class="block-div">
        <div class="block"></div>
        <div class="block"></div>
        <div class="block"></div>
        <div class="block"></div>
        <div class="block"></div>
        <div class="block"></div>
        <div class="block"></div>
        <div class="block"></div>
    </div>
</body>
</html>
```

* * *

* * *

* * *

###### 网格布局

```markup
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
            <meta content="width=device-width, initial-scale=1.0" name="viewport">
                <title>
                    grid布局
                </title>
                <style>
                    .demo {
                        width: 320px;
                        height: 320px;
                        border: 1px solid red;
                        /* 开启grid */
                        display: grid;
                        /* 设置行高和列宽 */
                        grid-template-rows: repeat(3, 1fr);
                        grid-template-columns: repeat(3, 1fr);
                        /* 设置行间距和列间距 */
                        gap: 10px;
                        /*gap: 10px 5px; 设置两个值的时候，第一个值是行间距，第二个值表示列间距*/
                    }

                    .demo div {
                        background-color: orange;
                        border: 1px solid black;
                    }
                    /**
                     * 人体成分分析与肌肉脂肪分析内容区
                     */
                    .content {
                        background: #fff;
                        /*border: 2px solid #4e4e4f;*/
                        border: 2px solid #4e4e4f;
                        height: 800px;
                        /*margin-top: 2mm;*/
                        display: grid;
                        grid-template: repeat(5, 1fr) / repeat(6, 1fr);
                        grid-template-areas: 'a b c d e f'
                                             'h h c d e m'
                                             'j j j d e o'
                                             'k k k k e p'
                                             'l l l l l q';
                    }

                    /*体内年龄*/
                    .content > .in-vivo-age {
                        grid-area: a;
                        /*background: cornflowerblue;*/
                        border: 2px solid #4e4e4f;
                    }

                    /*体内年龄值*/
                    .content > .in-vivo-age-value {
                        grid-area: b;
                        /*background: aquamarine;*/
                        border: 2px solid #4e4e4f;
                    }

                    /*体水分*/
                    .content > .body-moisture {
                        grid-area: h;
                        /*background: cadetblue;*/
                        border: 2px solid #4e4e4f;
                    }

                    /*蛋白质*/
                    .content > .protein {
                        grid-area: c;
                        border: 2px solid #4e4e4f;
                    }

                    /*肌肉量*/
                    .content > .muscle-mass {
                        grid-area: j;
                        border: 2px solid #4e4e4f;
                    }

                    /*去脂体重*/
                    .content > .lbm {
                        grid-area: k;
                        border: 2px solid #4e4e4f;
                    }

                    /*体重*/
                    .content > .weight {
                        grid-area: l;
                        border: 2px solid #4e4e4f;
                    }

                    .content > .estimated-bone-mass {
                        grid-area: d;
                        border: 2px solid #4e4e4f;
                    }

                    .content > .body-fat {
                        grid-area: e;
                        border: 2px solid #4e4e4f;
                    }

                    .content > .reference-value {
                        grid-area: f;
                        border: 2px solid #4e4e4f;
                    }

                    .content > .reference-value-1 {
                        grid-area: m;
                        border: 2px solid #4e4e4f;
                    }
                    .content > .reference-value-2 {
                        grid-area: o;
                        border: 2px solid #4e4e4f;
                    }
                    .content > .reference-value-3 {
                        grid-area: p;
                        border: 2px solid #4e4e4f;
                    }
                    .content > .reference-value-4 {
                        grid-area: q;
                        border: 2px solid #4e4e4f;
                    }
                </style>
            </meta>
        </meta>
    </head>
    <body>
        <div class="content">
            <div class="in-vivo-age">
            </div>
            <div class="in-vivo-age-value">
            </div>
            <div class="body-moisture">
            </div>
            <div class="protein">
            </div>
            <div class="estimated-bone-mass">
            </div>
            <div class="body-fat">
            </div>
            <div class="muscle-mass">
            </div>
            <div class="lbm">
            </div>
            <div class="weight">
            </div>
            <div class="reference-value">
            </div>
            <div class="reference-value-1">
            </div>
            <div class="reference-value-2">
            </div>
            <div class="reference-value-3">
            </div>
            <div class="reference-value-4">
            </div>
        </div>

        <div class="demo">
            <div>1</div>
            <div>2</div>
            <div>3</div>
            <div>4</div>
            <div>5</div>
            <div>6</div>
            <div>7</div>
            <div>8</div>
            <div>9</div>
        </div>
    </body>
</html>

```

* * *

* * *

* * *
