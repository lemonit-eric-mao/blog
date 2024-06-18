---
title: 迷你任务管理系统
date: '2023-05-15T12:37:59+00:00'
status: private
permalink: /2023/05/15/%e8%bf%b7%e4%bd%a0%e4%bb%bb%e5%8a%a1%e7%ae%a1%e7%90%86%e7%b3%bb%e7%bb%9f
author: 毛巳煜
excerpt: ''
type: post
id: 10021
category:
    - JavaScript
tag: []
post_format: []
wb_sst_seo:
    - 'a:3:{i:0;s:0:"";i:1;s:0:"";i:2;s:0:"";}'
---
```
<pre data-language="HTML">```markup



    <meta charset="UTF-8"></meta>
    <title>容器</title>

    <style>
        html, body, ul, li, div {
            padding: 0;
            margin: 0;
        }

        .panel {
            display: flex;
            flex-wrap: wrap;
            align-items: flex-start;
            justify-content: flex-start;
            padding: 5px;
        }

        .panel-item {
            width: 200px;
            height: 200px;
            margin: 5px;
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center;
            cursor: move;
            overflow: hidden;
        }
    </style>



<div class="panel">
    <div class="panel-item" style="background-image: url(https://picsum.photos/200/200/?random);"></div>
    <div class="panel-item" style="background-image: url(https://picsum.photos/300/250/?random);"></div>
    <div class="panel-item" style="background-image: url(https://picsum.photos/350/200/?random);"></div>
    <div class="panel-item" style="background-image: url(https://picsum.photos/200/300/?random);"></div>
    <div class="panel-item" style="background-image: url(https://picsum.photos/200/250/?random);"></div>
    <div class="panel-item" style="background-image: url(https://picsum.photos/100/200/?random);"></div>
    <div class="panel-item" style="background-image: url(https://picsum.photos/200/200/?random);"></div>
    <div class="panel-item" style="background-image: url(https://picsum.photos/300/250/?random);"></div>
    <div class="panel-item" style="background-image: url(https://picsum.photos/350/200/?random);"></div>
    <div class="panel-item" style="background-image: url(https://picsum.photos/200/300/?random);"></div>
    <div class="panel-item" style="background-image: url(https://picsum.photos/200/250/?random);"></div>
    <div class="panel-item" style="background-image: url(https://picsum.photos/100/200/?random);"></div>
    <div class="panel-item" style="background-image: url(https://picsum.photos/200/200/?random);"></div>
    <div class="panel-item" style="background-image: url(https://picsum.photos/300/250/?random);"></div>
    <div class="panel-item" style="background-image: url(https://picsum.photos/350/200/?random);"></div>
    <div class="panel-item" style="background-image: url(https://picsum.photos/200/300/?random);"></div>
    <div class="panel-item" style="background-image: url(https://picsum.photos/200/250/?random);"></div>
    <div class="panel-item" style="background-image: url(https://picsum.photos/100/200/?random);"></div>
</div>

<script>
    const panel = document.querySelector('.panel');
    const panelItems = [];

    /**
     * &#21021;&#22987;&#21270;&#23481;&#22120;
     */
    function initPanel(panelItems) {
        panelItems.forEach(item => panel.appendChild(item));
    }

    /**
     * &#21021;&#22987;&#21270;&#26102;&#20026;&#38754;&#26495;&#28155;&#21152;&#20107;&#20214;
     */
    function initAddPanelItemEvent() {
        const initPanelItems = document.querySelectorAll('.panel-item');
        initPanelItems.forEach(panelItem => {
            panelItem.setAttribute('draggable', 'true');
            panelItem.addEventListener('dragstart', handleDragStart);
            panelItem.addEventListener('dragend', handleDragEnd);
            panelItem.addEventListener('dragover', handleDragOver);
            panelItems.push(panelItem);
        })
    }

    /**
     * &#25490;&#24207;&#23481;&#22120;
     */
    function sortPanel() {
        // &#33719;&#21462;&#27599;&#20010;&#38754;&#26495;&#30340;&#20301;&#32622;&#20449;&#24687;
        panelItems.forEach((item) => {
            const rect = item.getBoundingClientRect();
            item.dataset.top = rect.top;
            item.dataset.left = rect.left;
        });

        // &#26681;&#25454;&#20301;&#32622;&#20449;&#24687;&#25490;&#24207;&#23481;&#22120;
        panelItems.sort((item1, item2) => {
            const topDiff = item1.dataset.top - item2.dataset.top;
            return topDiff !== 0 ? topDiff : item1.dataset.left - item2.dataset.left;
        });

        // &#37325;&#26032;&#21021;&#22987;&#21270;&#23481;&#22120;
        initPanel(panelItems);
    }

    /**
     * &#22788;&#29702;&#25302;&#25341;&#24320;&#22987;&#30340;&#20107;&#20214;
     * @param event
     */
    function handleDragStart(event) {
        event.currentTarget.classList.add('dragging');
        event.dataTransfer.setData('text/plain', 'panel-item');
    }

    /**
     * &#22788;&#29702;&#25302;&#25341;&#32467;&#26463;&#30340;&#20107;&#20214;
     * @param event
     */
    function handleDragEnd(event) {
        event.currentTarget.classList.remove('dragging');
        sortPanel();
    }

    /**
     * &#22788;&#29702;&#25302;&#25341;&#36807;&#31243;&#20013;&#30340;&#20107;&#20214;
     * @param event
     */
    function handleDragOver(event) {
        event.preventDefault();
        // &#21028;&#26029;&#24403;&#21069;&#40736;&#26631;&#20301;&#32622;&#21644;&#34987;&#25302;&#25341;&#20803;&#32032;&#20301;&#32622;&#65292;&#20915;&#23450;&#25554;&#20837;&#30340;&#20301;&#32622;
        const draggingElement = document.querySelector('.dragging');
        const thisElement = event.currentTarget;
        if (draggingElement && draggingElement !== thisElement) {
            const rect = thisElement.getBoundingClientRect();
            const offsetX = event.clientX - rect.left;
            const offsetY = event.clientY - rect.top;
            if (offsetX > thisElement.offsetWidth / 2 || offsetY > thisElement.offsetHeight / 2) {
                panel.insertBefore(draggingElement, thisElement.nextElementSibling);
            } else {
                panel.insertBefore(draggingElement, thisElement);
            }
            sortPanel();
        }
    }

    /**
     * &#22788;&#29702;&#31383;&#21475;&#22823;&#23567;&#21464;&#21270;&#30340;&#20107;&#20214;
     */
    function handleWindowResize() {
        sortPanel();
    }

    window.addEventListener('resize', handleWindowResize);

    // &#20026;&#38754;&#26495;&#28155;&#21152;&#20107;&#20214;
    initAddPanelItemEvent();
    // &#21021;&#22987;&#21270;&#23481;&#22120;
    initPanel(panelItems);

</script>




```
```