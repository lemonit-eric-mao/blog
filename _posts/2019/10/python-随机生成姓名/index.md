---
title: "Python 随机生成姓名"
date: "2019-10-25"
categories: 
  - "python"
---

##### 前置条件

- Python 2.7.14
- `Python3` 不支持 `MySQLdb` 模块，需要用 `pymysql` 替代，`pymysql` 兼容 2.7.14 `pip install pymysql` 或 `pip3 install pymysql`
- [Python 仓库](https://pypi.org/ "Python 仓库")

##### modify\_name.py

```python
#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019/10/25 17:39
# @Author  : Eric.Mao
# @FileName: modify_name.py
# @Software: PyCharm
# @Blog    ：http://www.dev-share.top/

import pymysql
import random
import sys

# 强制转码
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


class ModifyName(object):
    def __init__(self):
        # 缓存所有不重复的姓名
        self.result_names = set()
        # 连接到MySQL数据库
        self.db = pymysql.connect(
            host="172.160.180.53",
            port=3306,
            user="root",
            password="123456",
            database="sbtest",
            charset='utf8',
            conv={pymysql.FIELD_TYPE.STRING: str}, # 以字符串的方式返回查询结果
            cursorclass=pymysql.cursors.DictCursor # 以列表字典的格式返回查询结果
        )
        # 使用cursor()方法获取操作游标
        self.cursor = self.db.cursor()
        # 姓集合
        self.surnames = ['赵', '钱', '孙', '李', '西', '吴', '郑', '王', '冯', '陈', '楮', '卫', '蒋', '沈', '韩', '杨',
                         '朱', '秦', '尤', '许', '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜',
                         '戚', '谢', '邹', '喻', '柏', '水', '窦', '章', '云', '苏', '潘', '葛', '奚', '范', '彭', '郎',
                         '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳', '酆', '鲍', '史', '唐',
                         '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
                         '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄',
                         '和', '穆', '萧', '尹', '赖']
        # 名集合
        self.names = ['爱', '安', '百', '邦', '宝', '保', '抱', '贝', '倍', '蓓', '本',
                      '必', '碧', '璧', '斌', '冰', '兵', '炳', '步', '彩', '曹', '昌', '长', '常', '超',
                      '朝', '陈', '晨', '成', '呈', '承', '诚', '崇', '楚', '传', '春', '纯', '翠', '村',
                      '殿', '丁', '定', '东', '冬', '二', '凡', '方', '芳', '昉', '飞', '菲', '纷', '芬',
                      '奋', '风', '峰', '锋', '凤', '芙', '福', '付', '复', '富', '改', '刚', '高', '阁',
                      '铬', '根', '庚', '耕', '公', '功', '冠', '光', '广', '归', '桂', '国', '海', '寒',
                      '翰', '昊', '浩', '荷', '红', '宏', '洪', '鸿', '厚', '华', '存', '大', '丹', '道',
                      '德', '登', '砥', '典', '佃', '小', '狗', '亲']

    # 生成姓名
    def generate_name(self):
        # 姓
        sur = self.surnames[random.randint(0, len(self.surnames) - 1)]
        # 名
        name = self.names[random.randint(0, len(self.names) - 1)] + self.names[random.randint(0, len(self.names) - 1)]
        return sur + name

    # 生成去重后姓名
    def generate_name_list(self, count):
        while len(self.result_names) < count:
            name = self.generate_name()
            self.result_names.add(name)
        self.result_names = list(self.result_names)

    # 处理逻辑
    def processor(self, ids):

        num = len(ids)
        print('获得数据（%s）条' % len(ids))

        # 生成 num 个不重复的姓名
        self.generate_name_list(num)

        print('生成（%s）个不重复姓名' % len(self.result_names))

        # 将SQL语句批量加入到事务中
        for i in range(num):
            # 拼接 SQL 更新语句
            sql = "UPDATE table_1 SET username = '%s' WHERE id = '%s'" % (self.result_names[i], ids[i][0])
            # 将SQL语句加入到事务中
            self.cursor.execute(sql)

        try:
            # 提交一批SQL语句到数据库执行
            self.db.commit()
            print('执行成功!')
        except:
            print('执行失败!')
            # 发生错误时回滚
            self.db.rollback()

    # 初始化
    def init(self):
        sql = "SELECT id FROM table_1 LIMIT 5000"
        # 执行SQL语句
        self.cursor.execute(sql)
        # 获取所有记录列表
        ids = self.cursor.fetchall()
        # 处理逻辑
        self.processor(ids)


if __name__ == '__main__':
    __this = ModifyName()
    # 启动程序
    __this.init()
```
