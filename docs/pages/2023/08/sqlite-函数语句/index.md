---
title: "SQLite 函数语句"
date: "2023-08-07"
categories: 
  - "sqlite"
---

### 查询语句

```sql
SELECT JSON_GROUP_ARRAY(
    JSON_OBJECT(
        'id', parent.id,
        'name', parent.name,
        'parentId', parent.parent_id,
        'startTime', parent.start_time,
        'endTime', parent.end_time,
        'childTask', (
            SELECT JSON_GROUP_ARRAY(
                JSON_OBJECT(
                    'id', child.id,
                    'name', child.name,
                    'parentId', child.parent_id,
                    'startTime', child.start_time,
                    'endTime', child.end_time
                )
            )
            FROM task AS child
            WHERE child.parent_id = parent.id
        )
    )
) AS json_data
FROM task AS parent
WHERE parent.parent_id = '';
```

> 在 `SQLite` 中，你可以使用 `json_group_array()` 函数将多行数据合并为一个 `JSON 数组`，并使用 `json_object()` 函数将每一行数据转换为一个 `JSON 对象`。

#### 查询结果

```json
[
    {
        "id": "2cdd65565888454aa9b958c68efc3b1c",
        "name": "Item1",
        "parentId": "",
        "startTime": "2023-01-01 12:00:00",
        "endTime": "2023-01-01 12:00:00",
        "childTask": [
            {
                "id": "1a09dce321eb47c4a5b5e822b1e3b8b8",
                "name": "Item2",
                "parentId": "2cdd65565888454aa9b958c68efc3b1c",
                "startTime": "2023-01-01 13:00:00",
                "endTime": "2023-01-01 13:00:00"
            },
            {
                "id": "dd1ebed06e854b91b2e7efedb44e8819",
                "name": "Item3",
                "parentId": "2cdd65565888454aa9b958c68efc3b1c",
                "startTime": "2023-01-01 14:00:00",
                "endTime": "2023-01-01 14:00:00"
            }
        ]
    },
    {
        "id": "6a56b3c7b3fe4c9b8218d03ef438d5ec",
        "name": "Item4",
        "parentId": "",
        "startTime": "2023-01-01 15:00:00",
        "endTime": "2023-01-01 15:00:00",
        "childTask": [
            {
                "id": "1042272f1c03426fa5d410b34d72020c",
                "name": "Item5",
                "parentId": "6a56b3c7b3fe4c9b8218d03ef438d5ec",
                "startTime": "2023-01-01 16:00:00",
                "endTime": "2023-01-01 16:00:00"
            }
        ]
    }
]
```
