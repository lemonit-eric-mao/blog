---
title: "HTML 5 任意拖拽"
date: "2021-01-28"
categories: 
  - "javascript"
---

##### **[H5拖拽](https://developer.mozilla.org/zh-CN/docs/Web/API/HTML_Drag_and_Drop_API "H5拖拽")**

* * *

###### **任意拖拽**

```javascript
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <style>
        html, body {
            padding: 0;
            margin: 0;
            border: 0;
        }

        /*地基*/
        .cn-foundation {
            position: fixed;
            top: 0;
            left: 0;
            background: rgba(0, 0, 0, 0);
            width: 100vw;
            height: 100vh;
            font-size: 14px;
            display: flex;
            align-items: stretch;
            flex-direction: column;
        }

        .cn-foundation > .cn-panel {
            background-color: #a6a9ff;
            width: 200px;
            height: 200px;
            position: absolute;
        }

    </style>
</head>
<body>
<div class="cn-foundation" id="cnFoundation"></div>

<script>
    /**
     * 监听拖拽事件
     * @param ev
     */
    class DragEvent {

        constructor(element) {

            let x = 0;
            let y = 0;

            element.ondragstart = (ev) => {
                // 记录鼠标点击的位置，与当前控件左上角的[X,Y]距离
                x = ev.offsetX;
                y = ev.offsetY;

                // 添加拖拽数据
                ev.dataTransfer.setData("text/html", ev.target.outerHTML);

                /*
                 * 定义拖拽效果
                 *  copy 表明被拖拽的数据将从它原本的位置拷贝到目标的位置。
                 *  move 表明被拖拽的数据将被移动。
                 *  link 表明在拖拽源位置和目标位置之间将会创建一些关系表格或是连接。
                 */
                ev.dataTransfer.dropEffect = "move";
                // 返回鼠标点击时的[X,Y]坐标位置
                this.dragStart(ev.clientX, ev.clientY, element, ev);
            };

            element.ondrag = (ev) => {
                // this.drag(ev.screenX, ev.screenY);
                // 持续返回鼠标点击时的[X,Y]坐标位置
                this.drag(ev.clientX, ev.clientY, element);
            };

            element.ondragend = (ev) => {
                // 返回鼠标抬起时的[X,Y]坐标位置
                this.dragEnd(ev.clientX - x, ev.clientY - y, element, ev);
            };
        }

        dragStart(x, y, element, ev) {
        }

        drag(x, y, element) {
        }

        dragEnd(x, y, element, ev) {
        }
    }


    /**
     * 测试使用
     * @type {HTMLElement}
     */
    function createHTML(panelData) {

        const cnFoundation = document.getElementById("cnFoundation");

        panelData.map((data, index) => {
            let cnPanel = document.createElement('div');
            cnPanel.classList.add('cn-panel');
            cnPanel.setAttribute('draggable', 'true');
            cnPanel.style.backgroundColor = data.backgroundColor;

            // 添加拖拽事件
            const dragEvent = new DragEvent(cnPanel);
            dragEvent.drag = (x, y, element) => {
                // console.log(element.nextSibling)
            };
            dragEvent.dragEnd = (x, y, element) => {
                element.style.left = `${x}px`;
                element.style.top = `${y}px`;
            };

            cnFoundation.appendChild(cnPanel);
        });
    }

    let panelData = [
        {x: 0, y: 0, backgroundColor: `#${Math.floor(Math.random() * 0xffffff).toString(16)}`},
        {x: 100, y: 200, backgroundColor: `#${Math.floor(Math.random() * 0xffffff).toString(16)}`}
    ];

    createHTML(panelData);

</script>

</body>
</html>
```
