---
title: 'HTML 5 任意拖拽'
date: '2021-01-28T03:49:14+00:00'
status: private
permalink: /2021/01/28/html-5-%e4%bb%bb%e6%84%8f%e6%8b%96%e6%8b%bd
author: 毛巳煜
excerpt: ''
type: post
id: 6847
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### **[H5拖拽](https://developer.mozilla.org/zh-CN/docs/Web/API/HTML_Drag_and_Drop_API "H5拖拽")**

- - - - - -

###### **任意拖拽**

```javascript



    <meta charset="UTF-8"></meta>
    <title>Title</title>
    <style>
        html, body {
            padding: 0;
            margin: 0;
            border: 0;
        }

        /*&#22320;&#22522;*/
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


<div class="cn-foundation" id="cnFoundation"></div>

<script>
    /**
     * &#30417;&#21548;&#25302;&#25341;&#20107;&#20214;
     * @param ev
     */
    class DragEvent {

        constructor(element) {

            let x = 0;
            let y = 0;

            element.ondragstart = (ev) => {
                // &#35760;&#24405;&#40736;&#26631;&#28857;&#20987;&#30340;&#20301;&#32622;&#65292;&#19982;&#24403;&#21069;&#25511;&#20214;&#24038;&#19978;&#35282;&#30340;[X,Y]&#36317;&#31163;
                x = ev.offsetX;
                y = ev.offsetY;

                // &#28155;&#21152;&#25302;&#25341;&#25968;&#25454;
                ev.dataTransfer.setData("text/html", ev.target.outerHTML);

                /*
                 * &#23450;&#20041;&#25302;&#25341;&#25928;&#26524;
                 *  copy &#34920;&#26126;&#34987;&#25302;&#25341;&#30340;&#25968;&#25454;&#23558;&#20174;&#23427;&#21407;&#26412;&#30340;&#20301;&#32622;&#25335;&#36125;&#21040;&#30446;&#26631;&#30340;&#20301;&#32622;&#12290;
                 *  move &#34920;&#26126;&#34987;&#25302;&#25341;&#30340;&#25968;&#25454;&#23558;&#34987;&#31227;&#21160;&#12290;
                 *  link &#34920;&#26126;&#22312;&#25302;&#25341;&#28304;&#20301;&#32622;&#21644;&#30446;&#26631;&#20301;&#32622;&#20043;&#38388;&#23558;&#20250;&#21019;&#24314;&#19968;&#20123;&#20851;&#31995;&#34920;&#26684;&#25110;&#26159;&#36830;&#25509;&#12290;
                 */
                ev.dataTransfer.dropEffect = "move";
                // &#36820;&#22238;&#40736;&#26631;&#28857;&#20987;&#26102;&#30340;[X,Y]&#22352;&#26631;&#20301;&#32622;
                this.dragStart(ev.clientX, ev.clientY, element, ev);
            };

            element.ondrag = (ev) => {
                // this.drag(ev.screenX, ev.screenY);
                // &#25345;&#32493;&#36820;&#22238;&#40736;&#26631;&#28857;&#20987;&#26102;&#30340;[X,Y]&#22352;&#26631;&#20301;&#32622;
                this.drag(ev.clientX, ev.clientY, element);
            };

            element.ondragend = (ev) => {
                // &#36820;&#22238;&#40736;&#26631;&#25260;&#36215;&#26102;&#30340;[X,Y]&#22352;&#26631;&#20301;&#32622;
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
     * &#27979;&#35797;&#20351;&#29992;
     * @type {HTMLElement}
     */
    function createHTML(panelData) {

        const cnFoundation = document.getElementById("cnFoundation");

        panelData.map((data, index) => {
            let cnPanel = document.createElement('div');
            cnPanel.classList.add('cn-panel');
            cnPanel.setAttribute('draggable', 'true');
            cnPanel.style.backgroundColor = data.backgroundColor;

            // &#28155;&#21152;&#25302;&#25341;&#20107;&#20214;
            const dragEvent = new DragEvent(cnPanel);
            dragEvent.drag = (x, y, element) => {
                // console.log(element.nextSibling)
            };
            dragEvent.dragEnd = (x, y, element) => {
                element.style.left = `<span class="katex math inline">{x}px`;
                element.style.top = `{y}px`;
            };

            cnFoundation.appendChild(cnPanel);
        });
    }

    let panelData = [
        {x: 0, y: 0, backgroundColor: `#<span class="katex math inline">{Math.floor(Math.random() * 0xffffff).toString(16)}`},
        {x: 100, y: 200, backgroundColor: `#{Math.floor(Math.random() * 0xffffff).toString(16)}`}
    ];

    createHTML(panelData);

</script>




```