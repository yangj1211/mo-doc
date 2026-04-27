# Source 插入

本篇文档将指导你使用 `source` 命令批量导入数据至 MatrixOne Intelligence。

## 语法结构

```
SOURCE /path/to/your/sql_script.sql;
```

`/path/to/your/sql_script.sql` 是 SQL 脚本文件的绝对路径。当执行此命令时，客户端会读取指定的 SQL 脚本文件，并执行其中包含的所有 SQL 语句。

## 教程示例

在本教程中将指导你如何使用 `source` 命令将数据从 MySQL 迁移至 MatrixOne Intelligence。

### 步骤

#### 1. MySQL 数据转储

你需要拥有对 MySQL 实例的完全访问权限。

首先，使用 `mysqldump` 将 MySQL 表结构和数据通过以下命令转储到一个文件中。如果你不熟悉如何使用 `mysqldump`，可参见 [mysqldump 教程](https://simplebackups.com/blog/the-complete-mysqldump-guide-with-examples/)。

```
mysqldump -h IP_ADDRESS -uUSERNAME -pPASSWORD -d DB_NAME1 DB_NAME2 ... OUTPUT_FILE_NAME.SQL
```

示例如下，使用命令将一个命名为 *test* 数据库的所有表结构和数据转储到一个名为 *a.sql* 的文件中。

```
mysqldump -h 127.0.0.1 -uroot -proot -d test > a.sql
```

#### 2. 导入至 MatrixOne Intelligence

将整个表结构和数据导入到 MatrixOne Intelligence 中。

1. 打开 MySQL 终端并连接到 MatrixOne Intelligence。

2. 创建数据库 `test`，进入到数据库 `test`。

2. 通过 `source` 命令将 *sql* 文件导入 MatrixOne Intelligence。

```
mysql> source /YOUR_PATH/a.sql
```

如果 *sql* 文件较大，可以使用如下命令在后台运行导入任务：

```
nohup mysql -h freetier-01.cn-hangzhou.cluster.matrixonecloud.cn -P 6001 -u 585b49fc_852b_4bd1_b6d1_d64bc1d8xxxx:admin:accountadmin  -p'$pwd' -e 'use dbname; source /YOUR_PATH/a.sql;' &
```

#### 3. 检查数据

导入成功后，使用如下 SQL 语句查看导入结果：

```sql
use test;
show tables;
select * from table_name;
```

## 限制说明

MatrixOne Intelligence 已经支持 MySQL 的建表语句，因此可以顺畅的将 MySQL 表迁移到 MatrixOne Intelligence 上。不过需要注意，在迁移过程中，不兼容 MySQL 部分关键字，如 `engine=` 等，在 MatrixOne Intelligence 中会被自动忽略，也不会影响表结构的迁移。
