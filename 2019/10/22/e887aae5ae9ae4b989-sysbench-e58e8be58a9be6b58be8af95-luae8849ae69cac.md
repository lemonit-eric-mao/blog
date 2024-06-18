---
title: '学习自定义 sysbench 压力测试 Lua脚本'
date: '2019-10-22T09:36:14+00:00'
status: publish
permalink: /2019/10/22/%e8%87%aa%e5%ae%9a%e4%b9%89-sysbench-%e5%8e%8b%e5%8a%9b%e6%b5%8b%e8%af%95-lua%e8%84%9a%e6%9c%ac
author: 毛巳煜
excerpt: ''
type: post
id: 5083
category:
    - Lua
    - 测试工具
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### bank\_transfer.lua

```lua
#!/usr/bin/env sysbench

-- 1. 设置参数默认值
sysbench.cmdline.options = {
    table_size = {"一张表多个条数据, 默认值为 1 万", 10000},
    tables = {"创建几张表, 默认创建一张表", 1},
    events_items = {"单个事务中多少条语句, 默认值为 5000 条", 5000}
}

-- 3. 连接数据库，并且根据配置批量创建数据
function cmd_prepare()
    local drv = sysbench.sql.driver()
    local con = drv:connect()
    -- 批量创建
    for i = sysbench.tid % sysbench.opt.threads + 1, sysbench.opt.tables, sysbench.opt.threads do
        create_table(drv, con, i)
    end
end

-- 2. 定义 prepare 命令触发的脚本
sysbench.cmdline.commands = {
    -- 执行批量导入数据函数
    prepare = {cmd_prepare, sysbench.cmdline.PARALLEL_COMMAND}
}


-- 4. 创建数据表、数据
function create_table(drv, con, table_num)
    print(string.format("Creating table 'table_%d'...", table_num))

    -- 1 编写SQL 建表语句
    local query = string.format([[
                                  CREATE TABLE table_%d(
                                    id INTEGER NOT NULL,
                                    big_data TEXT NOT NULL,
                                    PRIMARY KEY (id)
                                  )
                                ]], table_num)
    -- 执行SQL
    con:query(query)

    if (sysbench.opt.table_size > 0) then
        print(string.format("Inserting %d records into 'table_%d'", sysbench.opt.table_size, table_num))
    end


    -- 2 创建较大的数据
    local value = "我是大数据"

    -- 3 编写SQL创建数据
    query = "INSERT INTO table_" .. table_num .. "(id, big_data) VALUES"
    -- 编写插入语句前半部分
    con:bulk_insert_init(query)

    -- 编写多个VALUES
    for i = 1, sysbench.opt.table_size do
        query = string.format("(%d, '%s')", i, value)
        con:bulk_insert_next(query)
    end

    -- 编写语句结束
    con:bulk_insert_done()

end


-- 执行 cleanup 命令时触发的函数。(清空数据)
function cleanup()
    local drv = sysbench.sql.driver()
    local con = drv:connect()

    for i = 1, sysbench.opt.tables do
        print(string.format("Dropping table 'table_%d'...", i))
        con:query("DROP TABLE IF EXISTS table_" .. i)
    end
end


-- 执行 run 命令 触发的函数(开始压测)，也就是真正开启事务进行压测的函数
function event()

    -- 随机选择表
    local table_num = sysbench.rand.default(1, sysbench.opt.tables)
    -- 获取当前年月日时分秒
    local datetime = os.date("%Y-%m-%d %H:%M:%S")

    -- 连接数据库
    local drv = sysbench.sql.driver()
    local con = drv:connect()

    -- 1. 开启事务
    con:query("BEGIN")

    -- 在一个事务内循环执行 N 次
    local n = sysbench.opt.events_items
    for i = 1, n do
        -- 将更新数据语句加入到单个事务中
        --
        -- 测试 5000条
        local result = con:query(string.format([[ UPDATE table_%d SET big_data = '%s' WHERE id = %d ]], table_num, datetime, i))
        --
        -- 更新 30万 条, 前置条件先造出30万条数据，然后这里不加 where
        -- local result = con:query(string.format([[ UPDATE table_%d SET big_data = '%s' ]], table_num, datetime))
        --
        -- 更新 30万 条, 前置条件先造出30万条数据，分批次更新 添加 LIMIT
        -- local result = con:query(string.format([[ UPDATE table_%d SET big_data = '%s' LIMIT 5000 ]], table_num, datetime))
        --
        -- 删除 30万 条, 前置条件先造出30万条数据，然后这里不加 where
        -- local result = con:query(string.format([[ DELETE FROM table_%d ]], table_num))
        --
        -- 删除 30万 条, 前置条件先造出30万条数据，分批次删除 添加 LIMIT
        -- local result = con:query(string.format([[ DELETE FROM table_%d LIMIT 5000 ]], table_num))
    end

    -- 回滚事务
    -- con:query("ROLLBACK")

    -- 提交事务
    con:query("COMMIT")
end


```

##### 执行脚本

```ruby
# 导入数据
[tidb@dev10 tidb-tools]<span class="katex math inline">sysbench --config-file=config bank_transfer.lua prepare
# 执行压测
[tidb@dev10 tidb-tools]</span> sysbench --config-file=config bank_transfer.lua run
# 清除压测数据
[tidb@dev10 tidb-tools]$ sysbench --config-file=config bank_transfer.lua cleanup

```

###### 脚本自定义参数

- **`--tables`**=1 创建几张表, 默认创建一张表
- **`--table_size`**=10000 一张表多个条数据, 默认值为 1 万
- **`--events_items`**=5000 单个事务中多少条语句, 默认值为 5000 条
- [其它默认参数](https://www.lemonit.cn/2019/02/26/sysbench-%E5%8E%8B%E5%8A%9B%E6%B5%8B%E8%AF%95/ "其它默认参数")

```ruby
[tidb@dev10 tidb-tools]$ sysbench --config-file=config --tables=1 --table_size=10000 --events=1 --events_items=5000  bank_transfer.lua run

```

**解释：** 对一张表中，10000行数据，使用一个事务，每个事务中5000条sql，进行压测。不同的SQL语句，也要配合不同的压测条件

- - - - - -

##### 参考资料

###### [增强你的 sysbench - 给 TiDB 添加自定义测试](https://www.jianshu.com/p/30933e0bebe7 "增强你的 sysbench - 给 TiDB 添加自定义测试")