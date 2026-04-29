# 导入本地数据

本节将介绍如何将本地数据文件导入到 MatrixOne Intelligence 实例中，包括使用 Load Data Local 命令和 Source 命令进行数据导入。

## 使用 Load Data Local 命令导入

Load Data Local 命令是常用的数据导入方式，MatrixOne 实例支持使用 Load Data Local 命令从客户端所在的本地文件系统批量导入 csv 文件或 jsonline 文件。若需使用本地文件导入命令，需要在数据文件所在的服务器上启动客户端连接 MatrixOne Intelligence 实例，示例如下：

```sql
mysql -h <host> -P 6001 -u <user_name>  -p --local-infile
```

**注意**：如果需要使用本地文件导入，需要在连接 MatrixOne 实例时加上后缀 --local-infile

### 导入 csv 文件

**语法结构**

```sql
LOAD DATA LOCAL
INFILE 'filename'
INTO TABLE tbl_name
[{FIELDS | COLUMNS}
    [TERMINATED BY '<string>']
    [[OPTIONALLY] ENCLOSED BY '<string>']
]
[LINES
    [STARTING BY 'string']
    [TERMINATED BY 'string']
]
[IGNORE number {LINES | ROWS}]
[PARALLEL {'TRUE' | 'FALSE'}]
```

**参数说明**

| 参数                   | 值                 | 必须/可选 | 描述                                                      |
| ---------------------- | ------------------ | --------- | --------------------------------------------------------- |
| infile                 | string             | 必须      | 本地数据文件的地址                                       |
| table                  | string             | 必须      | 本地文件导入到的数据表，需要提前创建                     |
| fields terminated by   | string             | 可选      | 字段分隔符，默认为 ','                                   |
| fields enclosed by     | string             | 可选      | 字段包围符，默认为 '"'                                  |
| lines starting by      | string             | 可选      | 行开始位置，默认为空字符串 ''                          |
| lines terminated by    | string             | 可选      | 行终止符，默认为换行符 '\n'                            |
| ignore                | Number             | 可选      | 加载时要忽略的行                                         |
| parallel              | {'TRUE' | 'FALSE'}  | 可选      | 并行导入，jsonline 文件默认为 true                        |

**语法示例**

```sql
-- 将本地目录下的 lineorder_flat.tbl 数据集加载到 MatrixOne Intelligence 实例中的数据表 lineorder_flat
LOAD DATA LOCAL INFILE '/ssb-dbgen-path/lineorder_flat.tbl ' INTO TABLE lineorder_flat;
```

**限制**

加载 csv 格式支持 JSON 类型，但需确保 JSON 内不包含字段终止符号，否则 JSON 需要用双引号括起来，例如：

- 正确示例：`"{"a": 1, "b": 2}", 2`
- 错误示例：`{"a": 1, "b": 2}, 2`

### 导入 jsonlines 文件

**关于 jsonlines 格式**

JSON（JavaScript Object Notation）是一种轻量级的数据交换格式。JSONLines 是一种更方便存储结构化数据的格式，也称为换行符分隔的 JSON。每一行都是独立、完整和合法的 JSON 值，行与行之间采用 '\n' 作为分隔符。

MatrixOne Intelligence 对于 JSONLines 格式有一些要求，它只允许包含相同数据类型和普通结构的 JSON 对象或 JSON 数组。MatrixOne Intelligence 暂时不支持具有嵌套结构的 JSONLines 文件。

**有效 JSONLines 对象示例**

```json
{"id":1,"father":"Mark","mother":"Charlotte"}
{"id":2,"father":"John","mother":"Ann"}
{"id":3,"father":"Bob","mother":"Monika"}
```

**无效 JSONLines 对象示例（包含嵌套结构）**

```json
{"id":1,"father":"Mark","mother":"Charlotte","children":["Tom"]}
{"id":2,"father":"John","mother":"Ann","children":["Jessika","Antony","Jack"]}
{"id":3,"father":"Bob","mother":"Monika","children":["Jerry","Karol"]}
```

**有效 JSONLines 数组示例（类似于 csv 格式）**

```json
["Name", "Session", "Score", "Completed"]
["Gilbert", "2013", 24, true]
["Alexa", "2013", 29, true]
["May", "2012B", 14, false]
["Deloise", "2012A", 19, true]
```

**无效 JSONLines 数组示例（数据类型和列数不匹配）**

```json
["Gilbert", "2013", 24, true, 100]
["Alexa", "2013", "twenty nine", true]
["May", "2012B", 14, "no"]
["Deloise", "2012A", 19, true, 40]
```

因为 JSON 数据类型与 MatrixOne Intelligence 的数据类型不同，需要在导入 JSONlines 文件之前创建数据表，确保它们的数据类型匹配。

**语法结构**

```sql
LOAD DATA LOCAL
INFILE {"filepath"='<string>', "format"='jsonline', 'jsondata'='<string>', "compression"='<string>'}
INTO TABLE tbl_name
[IGNORE number {LINES | ROWS}]
[PARALLEL {'TRUE' | 'FALSE'}]
```

**参数说明**

| 参数         | 值     | 必须/可选 | 描述                                   |
| ------------ | ------ | --------- | -------------------------------------- |
| file_path    | string | 必须      | 完整的对象存储文件路径                |
| format       | csv/jsonline | 必须 | 对象存储文件格式，默认为 csv          |
| jsondata     | object/array | 可选 | JSON 数据格式                           |
| compression  | auto/none/bz2/gzip/lz4 | 可选 | 对象存储文件的压缩格式，默认为 'none' |
| IGNORE       | Number | 可选 | 加载时要忽略的行                         |
| PARALLEL     | true/false | 可选 | 并行导入，jsonline 文件默认为 true       |

**语法示例**

```sql
-- 将 /mo_data/ 目录路径下的 data.jl.gz gzip 压缩数据文件导入到 MatrixOne Intelligence 实例中的数据表 db1.a，并从第二行开始导入。


LOAD DATA LOCAL INFILE {'filepath'='/mo_data/data.jl.gz', 'compression'='gzip','format'='jsonline','jsondata'='array'} into table db1.a ignore 1 lines;
```

## 使用 Source 命令导入

MatrixOne Intelligence 支持使用 SOURCE 命令从外部 SQL 脚本文件执行 SQL 语句，从而导入整个数据库结构（包括表结构和数据）。需要注意的是，当处理大量数据时，性能可能不如 LOAD DATA 命令高，因为 SOURCE 命令需要解析和执行每个 SQL 语句。

**语法结构**

```sql
SOURCE /<your_path>/sql_script.sql;
```

如果 SQL 文件较大，你可以使用以下命令在后台运行导入任务：

```sql
nohup mysql -h <moc_host> -P 6001 -u <user_name> -p<your_password> -D<databasename> -e 'source /<your_path>/a.sql;' &
```

## 限制

MatrixOne Intelligence 已经支持 MySQL 的建表语句，因此可以顺利将 MySQL 表迁移到 MatrixOne Intelligence。然而，需要注意，MatrixOne Intelligence 不兼容一些 MySQL 关键字，如 `engine=` 等，在 MatrixOne Intelligence 中会被自动忽略，不会影响表结构的迁移。如果要迁移的表中包含不兼容的数据类型、触发器、函数或存储过程，需要手动修改。更多关于兼容性的信息，请参阅 MySQL 兼容性。
