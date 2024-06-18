---
title: 'JavaScript开发, Web文件管理器'
date: '2021-01-27T03:33:15+00:00'
status: private
permalink: /2021/01/27/javascript%e5%bc%80%e5%8f%91-web%e6%96%87%e4%bb%b6%e7%ae%a1%e7%90%86%e5%99%a8
author: 毛巳煜
excerpt: ''
type: post
id: 6838
category:
    - JavaScript
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
###### 原生JS开发，文件管理器

```javascript



    <meta charset="UTF-8"></meta>
    <title></title>

    
    <style>
        html, body {
            padding: 0;
            margin: 0;
            border: 0;
            font-size: 14px;
        }

        /*&#22320;&#22522;*/
        .cn-foundation {
            position: fixed;
            top: 0;
            left: 0;
            /*&#26631;&#35782;&#32972;&#26223;&#36879;&#26126;&#65292;&#24182;&#19988;&#19981;&#24433;&#21709;&#23376;&#23618;&#30340;&#36879;&#26126;&#24230;*/
            background: rgba(0, 0, 0, 0);
            /*&#20805;&#28385;&#23631;&#24149;*/
            width: 100vw;
            height: 100vh;
            /*&#20351;&#29992;flexbox&#24067;&#23616;&#65292;&#35201;&#24819;&#20351;&#29992;flexbox&#27599;&#19968;&#23618;&#37117;&#24471;&#20889;display: flex;&#65292;&#23376;&#23618;&#19981;&#20250;&#32487;&#25215;&#29238;&#23618;&#30340;flexbox*/
            display: flex;
            align-items: stretch;
            flex-direction: column;
        }

        /*&#22320;&#38754;*/
        .cn-foundation > .cn-wrapper {
            position: relative;
            width: 100%;
            height: 100%;
        }

        /*&#24067;&#23616;-&#24038;&#20391;&#26641;*/
        .cn-foundation > .cn-wrapper > .left-wrapper {
            position: absolute;
            /* &#32477;&#23545;&#23450;&#20301;&#24773;&#20917; [&#19978; &#19979; &#24038; &#21491;]&#20805;&#28385;*/
            top: 0;
            bottom: 0;
            left: 0;
            right: 0;
            width: 10%;
        }

        /*&#20004;&#20010;&#24067;&#23616;&#20013;&#38388;&#30340;&#32447;*/
        .cn-foundation > .cn-wrapper > .left-wrapper > .line {
            position: absolute;
            top: 0;
            bottom: 0;
            right: 0;
            width: 2px;
            background-color: #999;
            z-index: 7;
            cursor: ew-resize;
        }

        /*&#24067;&#23616;-&#21491;&#20391;&#31649;&#29702;&#22120;*/
        .cn-foundation > .cn-wrapper > .right-wrapper {
            position: absolute;
            top: 0;
            bottom: 0;
            right: 0;
            width: 90%;
            display: flex;
            /*align-items: stretch;*/
            flex-direction: column;
        }

        /*&#26641;&#25972;&#20307;&#26679;&#24335;*/
        .left-cn-tree {
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: stretch;
        }

        /*&#27599;&#34892;&#20803;&#32032;&#26679;&#24335;*/
        .cn-item {
            padding-left: 10px;
            display: flex;
            flex-direction: column;
            align-items: stretch;
            cursor: move;
        }

        /*&#33410;&#28857;&#26679;&#24335;*/
        .cn-item > .cn-node {
            display: flex;
            align-items: center;
        }

        /*&#25991;&#20214;/&#25991;&#20214;&#22841;&#30340;&#22270;&#26631;&#26679;&#24335;*/
        .cn-item > .cn-node > .cn-icon {
            padding: 5px;
            width: 16px;
            height: 16px;
            display: flex;
            align-items: center;
            background-repeat: no-repeat; /** &#19981;&#37325;&#22797;*/
            background-size: contain; /**&#31561;&#27604;&#20363;&#32553;&#25918;*/
        }

        /*&#25991;&#20214;&#22841;&#25171;&#24320;&#30340;&#22270;&#26631;*/
        .dir-open {
            background-image: url('data:image/png;base64,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');
        }

        /*&#25991;&#20214;&#22841;&#20851;&#38381;&#30340;&#22270;&#26631;*/
        .dir-close {
            background-image: url('data:image/png;base64,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');
        }

        /*&#25991;&#20214;&#30340;&#22270;&#26631;*/
        .file {
            background-image: url('data:image/png;base64,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');
        }

        /*&#25991;&#20214;&#21517;*/
        .cn-item > .cn-node > .cn-name {
            padding: 5px;
            display: flex;
            align-items: center;
        }

        /*&#22238;&#25910;&#31449;*/
        .cn-recycle {
            position: absolute;
            /* [&#19979; &#24038; &#21491;]&#20805;&#28385;*/
            bottom: 0;
            left: 0;
            right: 0;
            background-color: rgba(245, 108, 108, 0.5);
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        /** ================================= &#20197;&#19979;&#20026;&#21491;&#20391;&#23548;&#33322; =============================== */
        .cn-foundation > .cn-wrapper > .right-wrapper > .right-nav {
            padding-left: 10px;
            height: 30px;
            display: flex;
            border-bottom: black 1px solid;
            align-items: center;
        }

        /*&#26641;&#25972;&#20307;&#26679;&#24335;*/
        .cn-foundation > .cn-wrapper > .right-wrapper > .right-cn-tree {
            padding-top: 10px;
            height: 100%;
            display: flex;
            align-items: start;
            flex-direction: column;
        }

    </style>



<div class="cn-foundation" id="foundation">

    
    <div class="cn-wrapper">
        
        <div class="left-wrapper" id="leftWrapper">
            <div class="left-cn-tree" id="leftCnTree"></div>
            <div class="cn-recycle" id="leftCnRecycle">回收站</div>
            
            <div class="line" id="cnLine"></div>
        </div>
        
        <div class="right-wrapper" id="rightWrapper">
            <div class="right-nav" id="rightNav"></div>
            <div class="right-cn-tree" id="rightCnTree"></div>
        </div>
    </div>
</div>

<script>

    /**
     * &#25991;&#20214;&#31649;&#29702;&#22120;
     */
    class FileManager {

        constructor(data) {
            // &#24038;&#20391;&#26641;
            let leftCnTree = document.getElementById('leftCnTree');
            // &#20013;&#38388;&#32447;
            let cnLine = document.getElementById('cnLine');
            // &#22238;&#25910;&#31449;
            let leftCnRecycle = document.getElementById('leftCnRecycle');
            // &#21491;&#20391;&#26641;
            this.rightCnTree = document.getElementById('rightCnTree');
            this.rightNav = document.getElementById('rightNav');

            // &#26500;&#24314;&#24038;&#20391;&#26641;
            this.buildLeftTree(leftCnTree, data);

            // &#20013;&#38388;&#32447;&#25302;&#21160;
            this.drapLine(cnLine);

            // &#26500;&#24314;&#21491;&#20391;&#26641;
            this.buildRecycle(leftCnRecycle);

            // &#28155;&#21152;&#19978;&#20256;&#25554;&#20214;
            this.fileUpload(this.rightCnTree);
        }


        /** ==================================== &#20197;&#19979; &#24038;&#20391;&#26641;&#20989;&#25968;&#21306;&#22495; ================================== */

        /**
         * &#25302;&#25341;&#20013;&#38388;&#32447;&#25913;&#21464;&#24067;&#23616;&#22823;&#23567;
         * @param element &#35201;&#32465;&#23450;&#30340;&#20803;&#32032;
         */
        drapLine(element) {
            // &#24038;&#20391;&#24067;&#23616;
            let leftWrapper = document.getElementById('leftWrapper');
            // &#21491;&#20391;&#24067;&#23616;
            let rightWrapper = document.getElementById('rightWrapper');

            let rightOffsetWidth = rightWrapper.clientWidth + leftWrapper.clientWidth;

            // &#32465;&#23450;&#40736;&#26631;&#25353;&#19979;&#20107;&#20214;
            element.onmousedown = (ev) => {
                ev.preventDefault();

                // &#25353;&#19979;&#26102;&#65292;&#30417;&#25511;&#30340;&#26159;document&#40736;&#26631;&#20107;&#20214;&#65292;&#19981;&#33021;&#20351;&#29992; cnLine&#23545;&#35937;&#32465;&#23450;&#65292;&#22240;&#20026;&#20107;&#20214;&#26377;&#25928;&#21306;&#22495;&#22826;&#23567;&#20102;
                document.onmousemove = (ev) => {
                    let x = ev.clientX;
                    leftWrapper.style.width = `<span class="katex math inline">{x}px`;
                    rightWrapper.style.width = `{rightOffsetWidth - x}px`;
                };
                document.onmouseup = () => {
                    // &#31227;&#38500;&#20107;&#20214;
                    document.onmousemove = null;
                    document.onmouseup = null;
                };
            };

        }


        /**
         * &#26500;&#24314;&#24038;&#20391;&#26641;
         * @param rootTree &#26641;&#26681;
         * @param treeData &#25968;&#25454;&#28304;
         * @param childNode &#26641;&#26525;/&#26641;&#21494;&#65288;&#23376;&#32423;&#23545;&#35937;&#65289;
         */
        buildLeftTree(rootTree, treeData, childNode) {

            // &#27169;&#26495;
            let template = `
                <div class="cn-node">
                    <i class="cn-icon">
                    <label class="cn-name">
                
                <div class="cn-child">
            `;

            // &#36845;&#20195;&#21019;&#24314;&#26641;
            treeData.map((item, index, sourceData) => {
                // &#21019;&#24314;Item
                let cnItem = document.createElement('div');
                // &#21019;&#24314;item
                cnItem.classList.add('cn-item', `${item.filepath}`);
                // &#20026;item&#28155;&#21152;&#26679;&#24335;
                cnItem.innerHTML = template;

                // &#21019;&#24314;Item&#23376;&#32423;&#20803;&#32032;
                let cnIcon = cnItem.querySelector('.cn-node > .cn-icon');
                let cnName = cnItem.querySelector('.cn-node > .cn-name');
                let cnChild = cnItem.querySelector('.cn-child');

                // &#25991;&#20214;/&#25991;&#20214;&#22841;&#21517;&#31216;
                cnName.innerHTML = item.filename;

                // &#28155;&#21152;&#25991;&#20214;/&#25991;&#20214;&#22841;&#22270;&#26631;
                let types = {dir: 'dir-close', file: 'file'};
                cnIcon.classList.add(types[item.type]);

                // &#40664;&#35748;&#38544;&#34255;&#23376;&#32423;
                cnChild.style.display = 'none';

                // &#25991;&#20214;&#22841;&#25171;&#24320;/&#20851;&#38381;, &#28857;&#20987;&#20107;&#20214;
                cnItem.onclick = (ev) => {
                    ev.stopPropagation();
                    if (cnChild.style.display) {
                        cnChild.style.display = '';
                        cnIcon.classList.add('dir-open');
                        cnIcon.classList.remove('dir-close');
                    } else {
                        cnChild.style.display = 'none';
                        cnIcon.classList.add('dir-close');
                        cnIcon.classList.remove('dir-open');
                    }

                    // &#25991;&#20214;&#22841;&#25171;&#24320;/&#20851;&#38381;, &#21160;&#30011;
                    cnChild.animate([
                        {opacity: 0},
                        {opacity: 1}
                    ], {
                        duration: 300
                    });

                    // item&#28857;&#20987;&#20999;&#25442;&#21491;&#20391;&#33756;&#21333;&#20107;&#20214;
                    this.leftItemClickSwitchMenu(item, rootTree);
                    // item&#28857;&#20987;&#22238;&#35843;&#20107;&#20214;
                    this.leftItemClickCallback(item, rootTree);
                };

                // &#21028;&#26029;&#24403;&#21069;&#25968;&#25454;&#20013;&#26159;&#21542;&#26377;&#23376;&#32423;&#25968;&#25454;
                if (item.child.length) {
                    this.buildLeftTree(rootTree, item.child, cnChild);
                }

                // &#21521;&#23376;&#32423;&#23545;&#35937;&#25110;&#32773;&#29238;&#32423;&#23545;&#35937;&#65292;&#25554;&#20837;&#20803;&#32032;
                let tree = childNode || rootTree;
                tree.appendChild(cnItem);
            });

        }

        /**
         * &#24038;&#20391;item&#28857;&#20987;&#20999;&#25442;&#21491;&#20391;&#33756;&#21333;&#20107;&#20214;
         * @param item
         */
        leftItemClickSwitchMenu(item, rootTree) {

            // &#25913;&#21464;&#21491;&#20391;&#23548;&#33322;
            this.rightSetNavicator(item.filepath);

            // &#25913;&#21464;&#21491;&#20391;&#25991;&#20214;&#21015;&#34920;
            if (item.type === 'file')
                return;
            this.rightCnTree.innerHTML = '';
            this.buildRightTree(this.rightCnTree, item.child);
        }


        /** ==================================== &#20197;&#19979; &#24038;&#20391;&#22238;&#25910;&#31449;&#20989;&#25968;&#21306;&#22495; ================================== */


        /**
         * &#28155;&#21152;&#22238;&#25910;&#31449;
         */
        buildRecycle(recycle) {
            // &#25345;&#32493;&#25509;&#25910;&#26032;&#20837;&#20803;&#32032;&#20107;&#20214;
            recycle.ondragover = (ev) => {
                ev.preventDefault();
                ev.dataTransfer.dropEffect = "move";
            };
            // &#22238;&#25910;&#31449;&#20107;&#20214;
            recycle.ondrop = (ev) => {
                ev.preventDefault();
                // &#33719;&#21462;&#25302;&#20837;&#22238;&#25910;&#31449;&#30340;&#25991;&#20214;&#30340;&#31867;&#26679;&#24335;
                let filepath = ev.dataTransfer.getData("item/filepath");
                // &#23558;&#31867;&#26679;&#24335;&#20013;&#30340;&#25991;&#20214;&#36335;&#24452;&#20256;&#32473;&#26381;&#21153;&#31471;&#36827;&#34892;&#21024;&#38500;
                if (!this.recycleCallback(filepath.replace('cn-item ', '')))
                    return;
                // &#26381;&#21153;&#31471;&#21024;&#38500;&#25104;&#21151;&#21518;&#65292;&#20877;&#21024;&#38500;&#39029;&#38754;&#20803;&#32032;
                let classNames = document.getElementsByClassName(filepath);
                for (let i = 0, len = classNames.length; i < len; i++) {
                    classNames[0].remove();
                }
            };
        }


        /** ==================================== &#20197;&#19979; &#21491;&#20391;&#26641;&#20989;&#25968;&#21306;&#22495; ================================== */


        /**
         * &#26500;&#24314;&#21491;&#20391;&#26641;
         * @param rootTree &#26641;&#26681;
         * @param treeData &#25968;&#25454;&#28304;
         * @param childNode &#26641;&#26525;/&#26641;&#21494;&#65288;&#23376;&#32423;&#23545;&#35937;&#65289;
         */
        buildRightTree(rootTree, treeData, childNode) {

            // &#27169;&#26495;
            let template = `
                <div class="cn-node">
                    <i class="cn-icon">
                    <label class="cn-name">
                
                <div class="cn-child">
            `;

            // &#36845;&#20195;&#21019;&#24314;&#26641;
            treeData.map((item, index, sourceData) => {
                // &#21019;&#24314;Item
                let cnItem = document.createElement('div');
                // &#21019;&#24314;class&#65292;&#24182;&#19988;&#23558;&#25991;&#20214;&#36335;&#24452;&#35774;&#32622;&#20026;&#31867;&#26679;&#24335;
                cnItem.classList.add('cn-item', `${item.filepath}`);
                // &#20026;item&#28155;&#21152;&#26679;&#24335;
                cnItem.innerHTML = template;
                // &#21487;&#25302;&#25341;
                cnItem.setAttribute('draggable', 'true');
                cnItem.ondragstart = (ev) => {
                    // &#28155;&#21152;&#25302;&#25341;&#25968;&#25454;, &#21482;&#33021;&#20256;&#23383;&#31526;&#20018;
                    // &#23558;&#31867;&#26679;&#24335;&#20570;&#20026;&#20256;&#36882;&#30340;&#21442;&#25968;
                    ev.dataTransfer.setData("item/filepath", ev.target.className);
                };

                // &#21019;&#24314;Item&#23376;&#32423;&#20803;&#32032;
                let cnIcon = cnItem.querySelector('.cn-node > .cn-icon');
                let cnName = cnItem.querySelector('.cn-node > .cn-name');
                let cnChild = cnItem.querySelector('.cn-child');

                // &#25991;&#20214;/&#25991;&#20214;&#22841;&#21517;&#31216;
                cnName.innerHTML = item.filename;

                // &#28155;&#21152;&#25991;&#20214;/&#25991;&#20214;&#22841;&#22270;&#26631;
                let types = {dir: 'dir-close', file: 'file'};
                cnIcon.classList.add(types[item.type]);

                // &#40664;&#35748;&#38544;&#34255;&#23376;&#32423;
                cnChild.style.display = 'none';

                // &#25991;&#20214;&#22841;&#25171;&#24320;/&#20851;&#38381;, &#28857;&#20987;&#20107;&#20214;
                cnItem.ondblclick = (ev) => {
                    ev.stopPropagation();
                    if (cnChild.style.display) {
                        cnChild.style.display = '';
                        cnIcon.classList.add('dir-open');
                        cnIcon.classList.remove('dir-close');
                    } else {
                        cnChild.style.display = 'none';
                        cnIcon.classList.add('dir-close');
                        cnIcon.classList.remove('dir-open');
                    }

                    // &#25991;&#20214;&#22841;&#25171;&#24320;/&#20851;&#38381;, &#21160;&#30011;
                    cnChild.animate([
                        {opacity: 0},
                        {opacity: 1}
                    ], {
                        duration: 300
                    });

                    // item&#28857;&#20987;&#20107;&#20214;
                    this.rightItemClick(item, rootTree);

                    // item&#28857;&#20987;&#22238;&#35843;&#20107;&#20214;
                    this.rightItemClickCallback(item, rootTree);
                };

                // &#21028;&#26029;&#24403;&#21069;&#25968;&#25454;&#20013;&#26159;&#21542;&#26377;&#23376;&#32423;&#25968;&#25454;
                if (item.child.length) {
                    this.buildRightTree(rootTree, item.child, cnChild);
                }

                // &#21521;&#23376;&#32423;&#23545;&#35937;&#25110;&#32773;&#29238;&#32423;&#23545;&#35937;&#65292;&#25554;&#20837;&#20803;&#32032;
                let tree = childNode || rootTree;
                tree.appendChild(cnItem);
            });

        }

        /**
         * &#21491;&#20391;item&#28857;&#20987;&#20107;&#20214;
         * @param item
         */
        rightItemClick(item, rootTree) {
            this.rightSetNavicator(item.filepath);
        }


        /** ==================================== &#20197;&#19979; &#21491;&#20391;&#23548;&#33322;&#20989;&#25968;&#21306;&#22495; ================================== */


        /**
         * &#35774;&#32622;&#21491;&#20391;&#23548;&#33322;
         * @param content
         */
        rightSetNavicator(content) {
            this.rightNav.innerHTML = content;
        }


        /** ==================================== &#20197;&#19979; &#25302;&#25341;&#19978;&#20256;&#20989;&#25968;&#21306;&#22495; ================================== */


        /**
         * &#25302;&#25341;&#19978;&#20256;
         * &#20351;&#29992;&#35828;&#26126;&#65306;
         *     // &#21491;&#20391;&#26641;
         *     this.rightCnTree = document.getElementById('rightCnTree');
         *     // &#28155;&#21152;&#19978;&#20256;&#25554;&#20214;
         *     this.fileUpload(this.rightCnTree);
         * @param element &#35201;&#32465;&#23450;&#30340;&#20803;&#32032;
         */
        fileUpload(element) {

            element.ondragover = (ev) => {
                // &#25991;&#20214;&#36827;&#20837;&#26102;&#26174;&#31034;&#34394;&#32447;&#26694;
                element.style.border = '1px dashed #26b58f';
                //&#38450;&#27490;&#40664;&#35748;&#35302;&#21457;
                ev.preventDefault();
                //&#38450;&#27490;&#20107;&#20214;&#20882;&#27873;
                ev.stopPropagation();
                return false;
            };
            element.ondrop = (ev) => {
                // &#40736;&#26631;&#25918;&#24320;&#26102;&#21435;&#25481;&#34394;&#32447;&#26694;
                element.style.border = '';
                ev.preventDefault();
                ev.stopPropagation();

                //&#33719;&#21462;&#20102;&#20174;&#22806;&#37096;&#25302;&#36827;&#26469;&#30340;&#25991;&#20214;
                const files = ev.dataTransfer.files;
                this.fileUploadCallback(files, element);
            }
        }

        /** ==================================== &#20197;&#19979; &#22238;&#35843;&#20989;&#25968;&#21306;&#22495; ================================== */


        /**
         * &#24038;&#20391;item&#28857;&#20987; &#22238;&#35843;&#20989;&#25968;
         * @param item
         */
        leftItemClickCallback(item, rootTree) {
        }

        /**
         * &#22238;&#25910;&#31449; &#22238;&#35843;&#20989;&#25968;
         * @param filepath &#35201;&#22238;&#25910;&#30340;&#25991;&#20214;&#25110;&#25991;&#20214;&#22841;&#36335;&#24452;
         * @returns {*} true|false
         */
        recycleCallback(filepath) {
            return filepath;
        }

        /**
         * &#21491;&#20391;item&#28857;&#20987; &#22238;&#35843;&#20989;&#25968;
         * @param item
         */
        rightItemClickCallback(item, rootTree) {
        }

        /**
         * &#25991;&#20214;&#19978;&#20256;&#22238;&#35843;&#20107;&#20214;
         * @param files &#29992;&#25143;&#19978;&#20256;&#30340;&#25991;&#20214;&#21015;&#34920;
         * @param element &#19978;&#20256;&#30340;&#25991;&#20214;&#35201;&#36861;&#21152;&#30340;&#21015;&#34920;
         */
        fileUploadCallback(files, element) {
            for (let i = 0, len = files.length; i < len; i++) {
                let file = files[i];

                // &#21019;&#24314;&#35835;&#21462;&#25991;&#20214;&#30340;&#23545;&#35937;,
                let fileReader = new FileReader();

                if (!file.type.includes('text')) {
                    alert('&#21482;&#20801;&#35768;&#19978;&#20256;&#25991;&#26412;&#25991;&#20214;&#65281;');
                    break;
                }

                // &#35299;&#20915;&#20013;&#25991;&#20081;&#30721;
                fileReader.readAsText(file, 'UTF-8');

                // &#25991;&#20214;&#20449;&#24687;&#35835;&#21462;&#23436;&#27605;&#20043;&#21518;&#35302;&#21457; fileReader.onload
                fileReader.onload = (param) => {
                    // &#25991;&#20214;&#21517;
                    console.log(file.name);
                    // &#25991;&#20214;&#20869;&#23481;
                    console.log(param.target.result);
                };
            }
        }


    }

    // &#25968;&#25454;&#28304;
    let data = [
        {
            filename: 'library',
            filepath: 'library/',
            type: 'dir',
            child: [
                {
                    filename: '&#19968;&#32423;',
                    filepath: '&#19968;&#32423;/',
                    type: 'dir',
                    child: [{
                        filename: '&#20108;&#32423;.docker',
                        filepath: '&#19968;&#32423;/&#20108;&#32423;.docker',
                        type: 'file',
                        child: []
                    }]
                },
                {
                    filename: '1&#32423;',
                    filepath: '1&#32423;/',
                    type: 'dir',
                    child: [
                        {
                            filename: '2-1&#32423;',
                            filepath: '1&#32423;/2-1&#32423;/',
                            type: 'dir',
                            child: [{
                                filename: '3-1&#32423;.docker',
                                filepath: '1&#32423;/2-1&#32423;/3-1&#32423;.docker',
                                type: 'file',
                                child: []
                            }]
                        },
                        {
                            filename: '2-2&#32423;',
                            filepath: '1&#32423;/2-2&#32423;/',
                            type: 'dir',
                            child: [{
                                filename: '3&#32423;',
                                filepath: '1&#32423;/2-2&#32423;/3&#32423;/',
                                type: 'dir',
                                child: []
                            }]
                        },
                        {
                            filename: '2-3&#32423;.txt',
                            filepath: '1&#32423;/2-3&#32423;.txt',
                            type: 'file',
                            child: []
                        }
                    ]
                }
            ]
        }

    ];
    // &#21021;&#22987;&#21270;
    const fileManager = new FileManager(data);

    fileManager.leftItemClickCallback = (item, rootTree) => {
    };

    fileManager.recycleCallback = (filepath) => {
        return true;
    };

    fileManager.rightItemClickCallback = (item, rootTree) => {
    };

</script>




```