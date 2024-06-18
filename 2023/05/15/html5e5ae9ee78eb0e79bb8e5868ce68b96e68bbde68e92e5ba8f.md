---
title: HTML5实现相册拖拽排序
date: '2023-05-15T12:04:17+00:00'
status: private
permalink: /2023/05/15/html5%e5%ae%9e%e7%8e%b0%e7%9b%b8%e5%86%8c%e6%8b%96%e6%8b%bd%e6%8e%92%e5%ba%8f
author: 毛巳煜
excerpt: ''
type: post
id: 10019
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



<div class="album"></div>

<script>
    const album = document.querySelector('.album');
    const albumItems = [];

    /**
     * &#21019;&#24314;&#19968;&#24352;&#30456;&#29255;&#30340;&#20803;&#32032;
     */
    function createAlbumItemElement(imageSrc) {
        const element = document.createElement('div');
        element.classList.add('album-item');
        element.style.backgroundImage = `url(${imageSrc})`;
        return element;
    }

    /**
     * &#21021;&#22987;&#21270;&#30456;&#20876;
     */
    function initAlbum(albumItems) {
        albumItems.forEach(item => album.appendChild(item));
    }

    /**
     * &#25490;&#24207;&#30456;&#20876;
     */
    function sortAlbum() {
        // &#33719;&#21462;&#27599;&#20010;&#30456;&#29255;&#30340;&#20301;&#32622;&#20449;&#24687;
        albumItems.forEach((item) => {
            const rect = item.getBoundingClientRect();
            item.dataset.top = rect.top;
            item.dataset.left = rect.left;
        });

        // &#26681;&#25454;&#20301;&#32622;&#20449;&#24687;&#25490;&#24207;&#30456;&#20876;
        albumItems.sort((item1, item2) => {
            const topDiff = item1.dataset.top - item2.dataset.top;
            return topDiff !== 0 ? topDiff : item1.dataset.left - item2.dataset.left;
        });

        // &#37325;&#26032;&#21021;&#22987;&#21270;&#30456;&#20876;
        initAlbum(albumItems);
    }

    /**
     * &#22788;&#29702;&#25302;&#25341;&#24320;&#22987;&#30340;&#20107;&#20214;
     * @param event
     */
    function handleDragStart(event) {
        event.currentTarget.classList.add('dragging');
        event.dataTransfer.setData('text/plain', 'album-item');
    }

    /**
     * &#22788;&#29702;&#25302;&#25341;&#32467;&#26463;&#30340;&#20107;&#20214;
     * @param event
     */
    function handleDragEnd(event) {
        event.currentTarget.classList.remove('dragging');
        sortAlbum();
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
                album.insertBefore(draggingElement, thisElement.nextElementSibling);
            } else {
                album.insertBefore(draggingElement, thisElement);
            }
            sortAlbum();
        }
    }

    /**
     * &#28155;&#21152;&#19968;&#24352;&#30456;&#29255;
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
     * &#22788;&#29702;&#31383;&#21475;&#22823;&#23567;&#21464;&#21270;&#30340;&#20107;&#20214;
     */
    function handleWindowResize() {
        sortAlbum();
    }

    window.addEventListener('resize', handleWindowResize);

    // &#28155;&#21152;&#19968;&#20123;&#38543;&#26426;&#30456;&#29255;
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
    // &#21021;&#22987;&#21270;&#30456;&#20876;
    initAlbum(albumItems);

</script>




```
```