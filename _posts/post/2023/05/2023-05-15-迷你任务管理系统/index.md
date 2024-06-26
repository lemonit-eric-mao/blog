---
title: "迷你任务管理系统"
date: "2023-05-15"
categories: 
  - "javascript"
---

```markup
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
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
</head>
<body>

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
     * 初始化容器
     */
    function initPanel(panelItems) {
        panelItems.forEach(item => panel.appendChild(item));
    }

    /**
     * 初始化时为面板添加事件
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
     * 排序容器
     */
    function sortPanel() {
        // 获取每个面板的位置信息
        panelItems.forEach((item) => {
            const rect = item.getBoundingClientRect();
            item.dataset.top = rect.top;
            item.dataset.left = rect.left;
        });

        // 根据位置信息排序容器
        panelItems.sort((item1, item2) => {
            const topDiff = item1.dataset.top - item2.dataset.top;
            return topDiff !== 0 ? topDiff : item1.dataset.left - item2.dataset.left;
        });

        // 重新初始化容器
        initPanel(panelItems);
    }

    /**
     * 处理拖拽开始的事件
     * @param event
     */
    function handleDragStart(event) {
        event.currentTarget.classList.add('dragging');
        event.dataTransfer.setData('text/plain', 'panel-item');
    }

    /**
     * 处理拖拽结束的事件
     * @param event
     */
    function handleDragEnd(event) {
        event.currentTarget.classList.remove('dragging');
        sortPanel();
    }

    /**
     * 处理拖拽过程中的事件
     * @param event
     */
    function handleDragOver(event) {
        event.preventDefault();
        // 判断当前鼠标位置和被拖拽元素位置，决定插入的位置
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
     * 处理窗口大小变化的事件
     */
    function handleWindowResize() {
        sortPanel();
    }

    window.addEventListener('resize', handleWindowResize);

    // 为面板添加事件
    initAddPanelItemEvent();
    // 初始化容器
    initPanel(panelItems);

</script>
</body>
</html>

```
