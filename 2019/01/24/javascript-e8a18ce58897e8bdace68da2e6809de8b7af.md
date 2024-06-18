---
title: 'JavaScript 行列转换思路'
date: '2019-01-24T09:05:40+00:00'
status: publish
permalink: /2019/01/24/javascript-%e8%a1%8c%e5%88%97%e8%bd%ac%e6%8d%a2%e6%80%9d%e8%b7%af
author: 毛巳煜
excerpt: ''
type: post
id: 3420
category:
    - JavaScript
tag: []
post_format: []
---
```
<pre data-language="HTML">```markup



    <meta charset="UTF-8"></meta>
    <link href="./jquery-3.3.1.min.js" rel="stylesheet"></link>
    
    <style type="text/css">
        table, tr, th, td {
            padding: 0px;
            margin: 0px;
        }

        table.gridtable {
            width: 1500px;
            font-family: verdana, arial, sans-serif;
            font-size: 11px;
            color: #333333;
            border-width: 1px;
            border-color: #666666;
            border-collapse: collapse;
        }

        table.gridtable th {
            border-width: 1px;
            padding: 8px;
            border-style: solid;
            border-color: #666666;
            background-color: #dedede;
        }

        table.gridtable td {
            border-width: 1px;
            padding: 8px;
            border-style: solid;
            border-color: #666666;
            background-color: #ffffff;
        }

        table.gridtable td > label {
            display: block;
            width: 100%;
            height: 100%;
            line-height: 100%;
            background: aqua;
        }
    </style>
    <script src="jquery-3.3.1.min.js"></script>


<input id="getDataId" type="button" value="获取结果！"></input>


<script>
    // &#21019;&#24314; table
    // &#21019;&#24314; thead
    // &#21019;&#24314; tr
    // &#21019;&#24314; th
    // &#21019;&#24314; tbody
    // &#21019;&#24314; tr
    // &#21019;&#24314; td

    var createTable = function () {
        return $('<table class="gridtable">');
    }

    var createThead = function () {
        var thead = $('<thead>');
        return thead;
    }

    var createTbody = function () {
        return $('<tbody id="tbodyId">')
    }

    var createTr = function () {
        return $('<tr>')
    }

    var createTh = function () {
        return $('<th>');
    }

    var createTd = function (id) {
        var td = (!id) ? $('<td>') : $('<td class="result-data" id="' + id + '" data="">');
        return td;
    }

    var createThRadio = function (index) {
        var radio = $('<input type="radio" name="th-radio-name" onclick="thRadioOnClick(' + index + ')" />');
        radio.prop('checked', index == 0);
        return radio;
    }

    var createTdRadio = function (i, j, spanText) {
        var label = $('<label>');
        var span = $('<span id="span-id-' + i + '-' + j + '">');
        span.text(spanText);
        var radio = $('<input type="radio" id="radio-id-' + i + '-' + j + '" name="radio-' + i + '" onclick="tdRadioOnClick(\'span-id-' + i + '-' + j + '\', \'td-id-' + i + '\')"/>');
        radio.prop('checked', j == 0);
        radio.appendTo(label);
        span.appendTo(label);
        return label;
    }

</script>


<script>
    function dataConvert(json) {
        // &#21019;&#24314;&#25968;&#25454;&#28304;
        // json = json || [{
        //     id: 10,
        //     name1: '&#21307;&#38498;0',
        //     name2: '&#21355;&#29983;&#38498;0',
        //     name3: '&#24314;&#27700;&#26446;&#28009;&#23528;&#23567;&#26103;&#37326;&#26449;&#21355;&#29983;&#25152;0',
        //     name4: '',
        //     name5: '1097593'
        // }, {
        //     id: 1,
        //     name1: '&#21307;&#38498;1',
        //     name2: '&#21355;&#29983;&#38498;1',
        //     name3: '&#24314;&#27700;&#26446;&#28009;&#23528;&#23567;&#26103;&#37326;&#26449;&#21355;&#29983;&#25152;1',
        //     name4: '',
        //     name5: '1097593'
        // }, {
        //     id: 2,
        //     name1: '&#21307;&#38498;2',
        //     name2: '&#21355;&#29983;&#38498;2',
        //     name3: '&#24314;&#27700;&#26446;&#28009;&#23528;&#23567;&#26103;&#37326;&#26449;&#21355;&#29983;&#25152;2',
        //     name4: '&#36797;&#23425;&#30465;',
        //     name5: '1097593'
        // }];

        // &#36716;&#25104;&#22914;&#19979;&#25968;&#25454;&#26684;&#24335;
        // var convertJson = [
        //     [{id: 0}, {id: 1}, {id: 2}],
        //     [{name1: '&#21307;&#38498;0'}, {name1: '&#21307;&#38498;1'}, {name1: '&#21307;&#38498;2'}],
        //     [{name2: '&#21355;&#29983;&#38498;0'}, {name1: '&#21355;&#29983;&#38498;1'}, {name2: '&#21355;&#29983;&#38498;2'}],
        //     [{name3: '&#24314;&#27700;&#26446;&#28009;&#23528;&#23567;&#26103;&#37326;&#26449;&#21355;&#29983;&#25152;0'}, {name3: '&#24314;&#27700;&#26446;&#28009;&#23528;&#23567;&#26103;&#37326;&#26449;&#21355;&#29983;&#25152;1'}, {name3: '&#24314;&#27700;&#26446;&#28009;&#23528;&#23567;&#26103;&#37326;&#26449;&#21355;&#29983;&#25152;2'}],
        //     [{name4: '&#36797;&#23425;&#30465;0'}, {name4: '&#36797;&#23425;&#30465;1'}, {name4: '&#36797;&#23425;&#30465;2'}],
        //     [{name5: '10975930'}, {name5: '10975931'}, {name5: '10975932'}],
        // ];

        var data = {};
        for (var i = 0; i < json.length; i++) {
            var item = json[i];
            for (k in item) {
                // &#21160;&#24577;&#29983;&#25104;&#19968;&#20010;&#23545;&#35937;
                var obj = {};
                obj[k] = item[k];
                // &#21019;&#24314; &#23384;&#25918;&#21516;&#19968;&#20010;key&#30340;&#25968;&#32452;
                var row = data[k] || [];
                row.push(obj);
                data[k] = row;
            }
        }
        // console.log(data);
        // &#21482;&#21462;&#25152;&#26377;&#23646;&#24615;&#21363;&#21487;
        var result = Object.values(data);
        $.fn.convertJson = result;
        // result.unshift(['&#26631;&#39064;&#19968;', '&#26631;&#39064;&#20108;', '&#26631;&#39064;&#19977;', '&#26631;&#39064;&#22235;', '&#26631;&#39064;&#20116;', '&#26631;&#39064;&#20845;']);
        // Object.assign(data, Object.values(data));
        return result;
    }
</script>


<script>
    var table = createTable();
    var thead = createThead();
    var tbody = createTbody();
    thead.appendTo(table);
    tbody.appendTo(table);
    <span class="katex math inline">('body').append(table);

    var createHead = function (convertJson) {
        var convertJson =.fn.convertJson;
        // &#31532;&#19968;&#23618;&#34920;&#22836;
        var tr = createTr();
        tr.appendTo(thead);

        var th = createTh('');
        th.appendTo(tr);
        th.text('&#23646;&#24615;');
        // &#20013;&#38388;&#21015;
        for (var i = 0; i < convertJson[0].length; i++) {
            var th = createTh('');
            th.appendTo(tr);
            th.text('&#35760;&#24405;' + i);
        }
        // &#39044;&#35272;&#21015;
        var th = createTh('');
        th.appendTo(tr);
        th.text('&#39044;&#35272;');

        // &#31532;&#20108;&#23618;&#34920;&#22836;
        var tr = createTr();
        tr.appendTo(thead);
        var th = createTh('');
        th.appendTo(tr);
        th.text('&#20027;&#35760;&#24405;');
        // &#20013;&#38388;&#21015;
        for (var i = 0; i < convertJson[0].length; i++) {
            var th = createTh('');
            th.appendTo(tr);
            createThRadio(i).appendTo(th);
        }
        // &#39044;&#35272;&#21015;
        var th = createTh('');
        th.appendTo(tr);
        th.text('-----');

    }
    var createBody = function (titles) {
        var convertJson = $.fn.convertJson;
        for (var i = 0; i < convertJson.length; i++) {
            var tr = createTr();
            tr.appendTo(tbody);
            // &#20027;&#23646;&#24615; &#20027;&#35760;&#24405;&#21015;
            var td = createTd();
            td.appendTo(tr);
            td.text(titles[i]);
            // &#25968;&#25454;&#21015;
            var child = convertJson[i];
            for (var j = 0; j < child.length; j++) {
                for (var key in child[j]) {
                    var td = createTd();
                    td.appendTo(tr);
                    if (child[j][key]) {
                        createTdRadio(i, j, child[j][key]).appendTo(td);
                    }
                }
            }
            // &#39044;&#35272; &#21015;
            var td = createTd('td-id-' + i);
            td.appendTo(tr);
        }
    }

    /**
     * th&#20013;&#30340; radio &#28857;&#20987;&#20107;&#20214;
     * @param spanId
     * @param tdId
     */
    function thRadioOnClick(colId) {
        resetRadio();
        $('#tbodyId > tr').each(function (index, tr) {
            // &#24403;&#21069;&#21015;&#25152;&#26377;&#36873;&#39033;&#20026;&#36873;&#20013;&#29366;&#24577;
            <span class="katex math inline">('#radio-id-' + index + '-' + colId).prop('checked', true);
            var span =('#span-id-' + index + '-' + colId);
            var spanText = span.text();

            // &#23558;&#36873;&#20013;&#30340;&#20540; &#36171;&#32473; &#39044;&#35272;&#21015;
            var td = <span class="katex math inline">('#td-id-' + index);
            td.text(spanText);
            // &#35760;&#24405;&#24403;&#21069;&#36873;&#20013;&#30340; &#34892;&#21015;&#20301;&#32622;
            var arr = [index, colId];
            td.attr("data", arr);
        });
    }

    /**
     * td&#20013;&#30340; radio &#28857;&#20987;&#20107;&#20214;
     * @param spanId
     * @param tdId
     */
    function tdRadioOnClick(spanId, tdId) {
        var arr = spanId.replace('span-id-', '').split('-');('#' + tdId).attr("data", arr);
        var spanText = <span class="katex math inline">('#' + spanId).text();('#' + tdId).text(spanText);
    }

    /**
     * &#37325;&#32622;&#25152;&#26377;radio&#36873;&#20013;&#29366;&#24577;
     */
    function resetRadio() {
        <span class="katex math inline">('tbody input[type="radio"]').each(function (index, radio) {(radio).prop('checked', false);
        });
    }

    /**
     * &#33719;&#21462;&#39044;&#35272;&#21015;&#35760;&#24405;&#30340;&#25152;&#26377;&#36873;&#20013;&#30340; &#34892;&#21015;&#20301;&#32622;
     */
    <span class="katex math inline">.fn.getResult = function () {
        var temp = [];('.result-data').each(function (i, td) {
            var result = $(td).attr('data');
            if (result) {
                temp.push(result);
            }
        });

        // &#26681;&#25454;&#34892;&#21015;&#20301;&#32622;&#65292; &#20174;&#20108;&#32500;&#25968;&#25454;&#20018;&#33719;&#21462;&#23545;&#24212;&#30340; &#23545;&#35937;&#25968;&#25454;
        var result = {};
        for (var i = 0; i < temp.length; i++) {
            var arr = temp[i].split(',');
            Object.assign(result, $.fn.convertJson[arr[0]][arr[1]]);
        }
        return result;
    }
</script>


<script>
    <span class="katex math inline">.fn.merge = function (title, json) {
        dataConvert(json);
        createHead();
        createBody(title);
    }
    var title = ['&#26631;&#39064;&#19968;', '&#26631;&#39064;&#20108;', '&#26631;&#39064;&#19977;', '&#26631;&#39064;&#22235;', '&#26631;&#39064;&#20116;', '&#26631;&#39064;&#20845;'];
    var json = [{
        id: 10,
        name1: '&#21307;&#38498;0',
        name2: '&#21355;&#29983;&#38498;0',
        name3: '&#24314;&#27700;&#26446;&#28009;&#23528;&#23567;&#26103;&#37326;&#26449;&#21355;&#29983;&#25152;0',
        name4: '',
        name5: '1097593'
    }, {
        id: 1,
        name1: '&#21307;&#38498;1',
        name2: '&#21355;&#29983;&#38498;1',
        name3: '&#24314;&#27700;&#26446;&#28009;&#23528;&#23567;&#26103;&#37326;&#26449;&#21355;&#29983;&#25152;1',
        name4: '',
        name5: '1097593'
    }, {
        id: 2,
        name1: '&#21307;&#38498;2',
        name2: '&#21355;&#29983;&#38498;2',
        name3: '&#24314;&#27700;&#26446;&#28009;&#23528;&#23567;&#26103;&#37326;&#26449;&#21355;&#29983;&#25152;2',
        name4: '&#36797;&#23425;&#30465;2',
        name5: '1097593'
    }];.fn.merge(title, json);
    <span class="katex math inline">('#getDataId').click(function () {
        console.log(.fn.getResult())
    });
</script>



```
```