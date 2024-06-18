---
title: Python读取Excel转sql
date: '2019-11-22T08:40:11+00:00'
status: publish
permalink: /2019/11/22/python%e8%af%bb%e5%8f%96excel%e8%bd%acsql
author: 毛巳煜
excerpt: ''
type: post
id: 5151
category:
    - Python
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### python 读取 excel 转 sql

###### 1 简单读取转换

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/22 17:34
# @Author  : Eric.Mao
# @FileName: excel-2-sql.py
# @Software: PyCharm
# @Blog    : https://www.lemonit.cn

import sys
import os
import xlrd
from datetime import date, datetime

reload(sys)
sys.setdefaultencoding('utf8')


class Excel2Sql(object):

    def __init__(self):
        self.file = 'www.xlsx'

    def read_excel(self):
        # 读取文件
        excel_file = xlrd.open_workbook(self.file)
        # 通过索引获取第一个Sheet
        sheet1 = excel_file.sheet_by_index(0)

        sql = "INSERT INTO organization ( orgnization_code , sfa_code , orgnization_name , orgnization_attribute , army_attribute , flow_attribute , level , grade , province , city , area , business_address , contact_person , contact_tel , postal_code , treat_scope , bed_space_no , daily_visit_no , in_hospital_no , longitude , latitude , status , norm_medical_terminal_code , hospital_level , assessment_province , industry_class , medical_and_health_classification , other_and_health_classification , retail_store_classification , is_virtual_hospital , dc_org_code , paas_id , paas_is_disable , paas_is_del , paas_create_time , paas_update_time , paas_create_user , paas_update_user , geographic_id )  VALUES  "
        values = []
        # 读取所有行(去掉标题行)
        for i in range(sheet1.nrows - 1):
            # 读取所有列
            value = []
            for col in sheet1.row_values(i + 1):
                value.append("'%s'" % col)
            values.append("(%s,uuid_short(),0,0,NOW(),NOW(),'superadmin','superadmin', 0)" % (','.join(value)))
        # 所有value
        result = sql + ','.join(values)

        self.save_file('./', 'chengda.sql', result)

    # 将生成的文件内容保存到本地
    def save_file(self, dist_dir, file_name, content):
        # 如果文件夹不存在
        if not os.path.exists(dist_dir):
            os.makedirs(dist_dir)
        #
        file = os.path.join(dist_dir, file_name)
        with open(file, 'w+') as f:
            f.write(content)
            f.close()


if __name__ == '__main__':
    # 初始化
    __this = Excel2Sql()
    # 启动程序
    __this.read_excel()


```

- - - - - -

###### 2 判断数据类型，做相应的处理

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/22 17:34
# @Author  : Eric.Mao
# @FileName: excel-2-sql.py
# @Software: PyCharm
# @Blog    : https://www.lemonit.cn

import sys
import os
import xlrd
import uuid
from xlrd import xldate_as_tuple
from datetime import date, datetime


class Excel2Sql(object):

    def __init__(self):
        self.file = 'file_name.xlsx'

    def read_excel(self):
        # 读取文件
        excel_file = xlrd.open_workbook(self.file)
        # 通过索引获取第一个Sheet
        sheet1 = excel_file.sheet_by_index(0)
        # 返回sheet1的行数
        nrows = sheet1.nrows
        # 返回sheet1的列数
        ncols = sheet1.ncols

        sql = "INSERT INTO dc_organization_master ( parent_id, organ_code, organ_name, organ_type, grade, drugstore_type, is_territory, paas_is_del, mdm_id, geography_id, paas_update_time, address, alias, first_in_terr_date, su, org_note, erp_code_one, qualified_hospital, tripartite_certification, paas_id )  VALUES  "
        values = []
        # 读取所有行(去掉标题行)
        for iRow in range(1, nrows):
            # 读取所有列
            value = []
            for iCol in range(ncols):
                # 每个单元格的值
                sCell = sheet1.cell_value(iRow, iCol)

                # 以下是要对Excel中的日期数据做类型转换
                # Python读Excel，返回的单元格内容的类型有5种：
                # ctype： 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
                ctype = sheet1.cell(iRow, iCol).ctype
                # ctype =3,为日期
                if ctype == 3:
                    date = datetime(*xldate_as_tuple(sCell, 0))
                    sCell = date.strftime('%Y/%m/%d %H:%M:%S')

                print(sCell)
                value.append("'%s'" % sCell)
            # 将 INSERT与VALUES合并
            values.append("(%s, '%s')" % (','.join(value), uuid.uuid1()))
        # 所有value
        result = sql + ','.join(values)
        # 生成新文件
        self.save_file('./', 'excel_2.sql', result)
        print('文件已经生成： ./excel_2.sql')

    # 将生成的文件内容保存到本地
    def save_file(self, dist_dir, file_name, content):
        # 如果文件夹不存在
        if not os.path.exists(dist_dir):
            os.makedirs(dist_dir)
        #
        file = os.path.join(dist_dir, file_name)
        with open(file, 'w+') as f:
            f.write(content)
            f.close()


if __name__ == '__main__':
    # 初始化
    __this = Excel2Sql()
    # 启动程序
    __this.read_excel()


```