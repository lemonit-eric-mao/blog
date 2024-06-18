---
title: 'Lua 自定义 sysbench 压力测试脚本'
date: '2019-10-31T09:07:42+00:00'
status: private
permalink: /2019/10/31/lua-%e8%87%aa%e5%ae%9a%e4%b9%89-sysbench-%e5%8e%8b%e5%8a%9b%e6%b5%8b%e8%af%95%e8%84%9a%e6%9c%ac
author: 毛巳煜
excerpt: ''
type: post
id: 5098
category:
    - Lua
    - 测试工具
tag: []
post_format: []
hestia_layout_select:
    - sidebar-right
---
##### create 测试数据库表

```sql
CREATE TABLE `dc_organization_master` (
`organ_code` VARCHAR ( 100 ) DEFAULT NULL,
`organ_name` VARCHAR ( 200 ) DEFAULT NULL,
`province` VARCHAR ( 100 ) DEFAULT NULL,
`city` VARCHAR ( 200 ) DEFAULT NULL,
`district` VARCHAR ( 500 ) DEFAULT NULL,
`address` VARCHAR ( 500 ) DEFAULT NULL,
`property_one` VARCHAR ( 32 ) DEFAULT NULL,
`merge_to` VARCHAR ( 200 ) DEFAULT NULL,
`parent_id` VARCHAR ( 100 ) DEFAULT NULL,
`organ_type` VARCHAR ( 32 ) DEFAULT NULL,
`level` VARCHAR ( 32 ) DEFAULT NULL,
`nature` VARCHAR ( 32 ) DEFAULT NULL,
`organ_used_names` VARCHAR ( 2000 ) DEFAULT NULL,
`is_territory` VARCHAR ( 32 ) DEFAULT NULL,
`su` VARCHAR ( 500 ) DEFAULT NULL,
`bai` VARCHAR ( 500 ) DEFAULT NULL,
`erp_code_one` VARCHAR ( 32 ) DEFAULT NULL,
`geography_id` VARCHAR ( 100 ) DEFAULT NULL COMMENT '地理信息ID',
`org_note` VARCHAR ( 500 ) DEFAULT NULL COMMENT '机构备注',
`grade` VARCHAR ( 32 ) DEFAULT NULL COMMENT 'grade',
`drugstore_type` VARCHAR ( 32 ) DEFAULT NULL COMMENT 'drugstoreType',
`alias` VARCHAR ( 500 ) DEFAULT NULL COMMENT 'alias',
`first_in_terr_date` VARCHAR ( 32 ) DEFAULT NULL COMMENT 'firstInTerrDate',
`erp_code` VARCHAR ( 32 ) DEFAULT NULL COMMENT 'ERPCode',
`paas_is_disable` VARCHAR ( 32 ) DEFAULT '0' COMMENT '系统是否有效',
`paas_create_user` VARCHAR ( 32 ) DEFAULT NULL COMMENT '系统创建人',
`paas_create_time` datetime DEFAULT NULL COMMENT '系统创建时间',
`paas_update_user` VARCHAR ( 32 ) DEFAULT NULL COMMENT '系统修改人',
`paas_update_time` datetime DEFAULT NULL COMMENT '系统修改时间',
`paas_version_no` VARCHAR ( 32 ) DEFAULT NULL COMMENT '系统版本号',
`paas_is_del` VARCHAR ( 32 ) DEFAULT '0' COMMENT '系统是否删除',
`paas_id` VARCHAR ( 100 ) NOT NULL,
`error_memo` VARCHAR ( 200 ) DEFAULT NULL COMMENT '错误描述',
`sync_time` datetime DEFAULT NULL COMMENT '同步时间',
`head_office_code` VARCHAR ( 100 ) DEFAULT NULL COMMENT '总店代码',
`head_office_name` VARCHAR ( 200 ) DEFAULT NULL COMMENT '总店名称',
`head_office_used_names` VARCHAR ( 2000 ) DEFAULT NULL COMMENT '总店曾用名',
`qualified_hospital` VARCHAR ( 200 ) DEFAULT NULL COMMENT '合格医院',
`tripartite_certification` VARCHAR ( 100 ) DEFAULT NULL COMMENT '三方认证',
`sap_code` VARCHAR ( 100 ) DEFAULT NULL COMMENT 'SAPCode',
`legal_entity` VARCHAR ( 100 ) DEFAULT NULL COMMENT 'Legal Entity',
`status` VARCHAR ( 32 ) DEFAULT NULL COMMENT '状态',
`operat_type` VARCHAR ( 32 ) DEFAULT NULL COMMENT '操作类型'
) ENGINE = INNODB DEFAULT CHARSET = utf8 COLLATE = utf8_bin COMMENT = '机构主数据';

```

- - - - - -

##### insert.lua

- `插入700万数据---1个事务，每个事务中7个SQL语句，每个语句1W个values；以每个事务7W数据进行插入`

```lua
#!/usr/bin/env sysbench

-- 执行 cleanup 命令时触发的函数。(清空数据)
function cleanup()
    local drv = sysbench.sql.driver()
    local con = drv:connect()
    print(string.format("Dropping table dc_organization_master"))
    con:query("DROP TABLE IF EXISTS dc_organization_master")
end


-- 执行 run 命令 触发的函数(开始压测)，也就是真正开启事务进行压测的函数
function event()

    -- 连接数据库
    local drv = sysbench.sql.driver()
    local con = drv:connect()

    for i = 1, 100 do

        -- 每个事务中7个SQL语句，每个语句1W个values；
        -- 1. 开启事务
        con:query("BEGIN")

        for j = 1, 7 do

            -- 编写SQL创建数据
            query = "INSERT INTO dc_organization_master VALUES"
            -- 编写插入语句前半部分
            con:bulk_insert_init(query)

            -- 生成 1W个VALUES
            for k = 1, 10000 do
                query = string.format("(NULL,'DS000000%d','江阴市海鹏医药有限公司张家港花园浜店','江苏','苏州市','张家港市','NULL',NULL,NULL,'E45593F1-B2BE-E711-9403-098571E','3',NULL,'2','姜names凤龙','1','PRE1B044',NULL,'NULL','11-A07D-0017D2CF','NULL','NULL','2','NULL','2017Q3','NULL','0',NULL,NULL,NULL,NULL,NULL,'0','PAAS-ID-%d',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'3',NULL)", k, k)
                con:bulk_insert_next(query)
            end

            -- 编写语句结束
            con:bulk_insert_done()

        end

        -- 提交事务
        con:query("COMMIT")
    end

end


```

###### config

```ruby
[root@dev10 ~]$ cat > config 
```

**执行**`[root@dev10 ~]$ sysbench --config-file=config insert.lua run`

- - - - - -

##### select.lua

```lua
#!/usr/bin/env sysbench

-- 执行 run 命令 触发的函数(开始压测)，也就是真正开启事务进行压测的函数
function event()

    -- 连接数据库
    local drv = sysbench.sql.driver()
    local con = drv:connect()

    for i = 1, 2 do

      -- 编写SQL创建数据
      sql = string.format("SELECT * FROM dc_organization_master LIMIT %d,10000", i * 10000)

      local result = con:query(sql)

      -- 打印第二列数据
      print(result:fetch_row()[2])

      -- 循环输入结果，使用 lua的unpack函数解析返回的结果(table)
      for j = 1, result.nrows do
          print(string.format("%s %s %s", unpack(result:fetch_row(), 1, result.nfields)))
      end

    end

end


```

###### **执行**

```ruby
[root@dev10 ~]$ sysbench --config-file=config select.lua run

```

- - - - - -

- - - - - -

- - - - - -