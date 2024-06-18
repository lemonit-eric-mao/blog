---
title: "HTML5实现相册拖拽排序"
date: "2023-05-15"
categories: 
  - "javascript"
---

```markup
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>相册</title>

    <style>
        html, body, ul, li, div {
            padding: 0;
            margin: 0;
        }

        .album {
            display: flex;
            flex-wrap: wrap;
            align-items: flex-start;
            justify-content: flex-start;
            padding: 5px;
        }

        .album-item {
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

<div class="album"></div>

<script>
    const album = document.querySelector('.album');
    const albumItems = [];

    /**
     * 创建一张相片的元素
     */
    function createAlbumItemElement(imageSrc) {
        const element = document.createElement('div');
        element.classList.add('album-item');
        element.style.backgroundImage = `url(${imageSrc})`;
        return element;
    }

    /**
     * 初始化相册
     */
    function initAlbum(albumItems) {
        albumItems.forEach(item => album.appendChild(item));
    }

    /**
     * 排序相册
     */
    function sortAlbum() {
        // 获取每个相片的位置信息
        albumItems.forEach((item) => {
            const rect = item.getBoundingClientRect();
            item.dataset.top = rect.top;
            item.dataset.left = rect.left;
        });

        // 根据位置信息排序相册
        albumItems.sort((item1, item2) => {
            const topDiff = item1.dataset.top - item2.dataset.top;
            return topDiff !== 0 ? topDiff : item1.dataset.left - item2.dataset.left;
        });

        // 重新初始化相册
        initAlbum(albumItems);
    }

    /**
     * 处理拖拽开始的事件
     * @param event
     */
    function handleDragStart(event) {
        event.currentTarget.classList.add('dragging');
        event.dataTransfer.setData('text/plain', 'album-item');
    }

    /**
     * 处理拖拽结束的事件
     * @param event
     */
    function handleDragEnd(event) {
        event.currentTarget.classList.remove('dragging');
        sortAlbum();
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
                album.insertBefore(draggingElement, thisElement.nextElementSibling);
            } else {
                album.insertBefore(draggingElement, thisElement);
            }
            sortAlbum();
        }
    }

    /**
     * 添加一张相片
     * @param imageSrc
     */
    function addAlbumItem(imageSrc) {
        const albumItem = createAlbumItemElement(imageSrc);
        albumItem.setAttribute('draggable', 'true');
        albumItem.addEventListener('dragstart', handleDragStart);
        albumItem.addEventListener('dragend', handleDragEnd);
        albumItem.addEventListener('dragover', handleDragOver);
        albumItems.push(albumItem);
        album.appendChild(albumItem);
    }

    /**
     * 处理窗口大小变化的事件
     */
    function handleWindowResize() {
        sortAlbum();
    }

    window.addEventListener('resize', handleWindowResize);

    // 添加一些随机相片
    addAlbumItem('https://picsum.photos/200/200/?random');
    addAlbumItem('https://picsum.photos/200/250/?random');
    addAlbumItem('https://picsum.photos/250/200/?random');
    addAlbumItem('https://picsum.photos/250/300/?random');
    addAlbumItem('https://picsum.photos/300/250/?random');
    addAlbumItem('https://picsum.photos/300/300/?random');
    addAlbumItem('https://picsum.photos/200/200/?random');
    addAlbumItem('https://picsum.photos/200/250/?random');
    addAlbumItem('https://picsum.photos/250/200/?random');
    addAlbumItem('https://picsum.photos/250/300/?random');
    addAlbumItem('https://picsum.photos/300/250/?random');
    addAlbumItem('https://picsum.photos/300/300/?random');
    // 初始化相册
    initAlbum(albumItems);

</script>
</body>
</html>

```
