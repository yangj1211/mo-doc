# 插入 csv 文件

本篇文档将指导你在 MySQL 客户端连接 MatrixOne Intelligence 时如何完成 *csv* 格式数据导入。

在使用 MatrixOne Intelligence 时，支持使用 `LOAD DATA LOCAL` 语法将位于**客户端主机**上的 *csv* 数据文件导入至 MatrixOne Intelligence 集群，详细语法可参考 [LOAD DATA 语法介绍](../../../Reference/SQL-Reference/Data-Manipulation-Language/load-data.md)。

__Note__: *CSV*（逗号分隔值）文件是一种特殊的文件类型，可在 Excel 中创建或编辑，*CSV* 文件不是采用多列的形式存储信息，而是使用逗号分隔的形式存储信息。MatrixOne 可使用的 *CSV* 格式需符合 **RFC4180** 标准。

## 语法结构

```
LOAD DATA LOCAL
INFILE 'file_name'
INTO TABLE tbl_name
[{FIELDS | COLUMNS}
[TERMINATED BY 'string']
[[OPTIONALLY] ENCLOSED BY 'char']
]
[LINES
[STARTING BY 'string']
[TERMINATED BY 'string']
]
[IGNORE number {LINES | ROWS}]
[PARALLEL {'TRUE' | 'FALSE'}]
```

## 在 MySQL Client 中使用 `Load data local` 命令导入数据

__Note__: 使用 `Load data local` 命令时，数据文件需位于执行该语句的 MySQL 客户端所在的服务器中。

### 步骤

1. 在 MatrixOne Intelligence 中创建对应的数据表。

2. 将数据文件拷贝至 MySQL 客户端所在的服务器中。

3. 使用 MySQL 客户端连接 MatrixOne Intelligence，例如：

    ```
    mysql -h freetier-01.cn-hangzhou.cluster.matrixonecloud.cn -P 6001 -u 585b49fc_852b_4bd1_b6d1_d64bc1d8xxxx:admin:accountadmin  -p --local-infile
    ```

4. 在 MySQL 客户端中执行 `LOAD DATA LOCAL` 命令：

    ```
    mysql> LOAD DATA LOCAL INFILE '/tmp/xxx.csv'
    INTO TABLE table_name
    FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY "\r\n";
    ```

## __限制__

加载 `csv` 格式支持 JSON 类型，但是需要确保 JSON 内不含有字段终止符号，如果 JSON 内含有字段终止符号，那么 JSON 需要用双引号包裹起来。例如：

- 正确示例：`"{"a":1, "b":2}", 2`
- 错误示例：`{"a":1, "b":2}, 2`
