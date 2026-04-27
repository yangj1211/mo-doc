# RESTORE ACCOUNT

## 语法说明

`RESTORE ACCOUNT` 根据当前实例下创建的快照将实例/数据库/表恢复到某个时间戳对应的状态。

## 语法结构

```
> RESTORE ACCOUNT account_name [DATABASE database_name [TABLE table_name]] FROM SNAPSHOT snapshot_name [TO ACCOUNT account_name];
```

## 示例

- 示例 1：恢复实例

```sql
--在实例 01907cb0-9b99-7714-8f1b-4b55c5eaxxxx 下执行
CREATE database db1;
CREATE database db2;

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| db1                |
| db2                |
| information_schema |
| mo_catalog         |
| mysql              |
| system             |
| system_metrics     |
+--------------------+
7 rows in set (0.12 sec)

create snapshot snap1 for account `01907cb0-9b99-7714-8f1b-4b55c5eaxxxx`; --创建快照
mysql> show snapshots;
+---------------+-------------------------------+----------------+--------------------------------------+---------------+------------+
| SNAPSHOT_NAME | TIMESTAMP                     | SNAPSHOT_LEVEL | ACCOUNT_NAME                         | DATABASE_NAME | TABLE_NAME |
+---------------+-------------------------------+----------------+--------------------------------------+---------------+------------+
| snap1         | 2024-07-09 07:12:55.869132523 | account        | 01907cb0-9b99-7714-8f1b-4b55c5eaxxxx |               |            |
+---------------+-------------------------------+----------------+--------------------------------------+---------------+------------+
1 row in set (0.12 sec)

drop database db1;--删除数据库 db1,db2
drop database db2;

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mo_catalog         |
| mysql              |
| system             |
| system_metrics     |
+--------------------+
5 rows in set (0.15 sec)

restore account  `01907cb0-9b99-7714-8f1b-4b55c5eaxxxx` FROM snapshot snap1;--恢复实例级别快照

mysql> show databases;--恢复成功
+--------------------+
| Database           |
+--------------------+
| db1                |
| db2                |
| information_schema |
| mo_catalog         |
| mysql              |
| system             |
| system_metrics     |
+--------------------+
7 rows in set (0.01 sec)
```

- 示例 2：恢复数据库

```sql
--在实例 01907cb0-9b99-7714-8f1b-4b55c5eaxxxx 下执行
CREATE database db1;

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| db1                |
| information_schema |
| mo_catalog         |
| mysql              |
| system             |
| system_metrics     |
+--------------------+
7 rows in set (0.00 sec)

create snapshot db_snap1 for account `01907cb0-9b99-7714-8f1b-4b55c5eaxxxx`;--创建快照
drop database db1;--删除数据库 db1

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mo_catalog         |
| mysql              |
| system             |
| system_metrics     |
+--------------------+
6 rows in set (0.01 sec)

restore account `01907cb0-9b99-7714-8f1b-4b55c5eaxxxx` database db1 FROM snapshot db_snap1;--恢复数据库级别快照

mysql> show databases;--恢复成功
+--------------------+
| Database           |
+--------------------+
| db1                |
| information_schema |
| mo_catalog         |
| mysql              |
| system             |
| system_metrics     |
+--------------------+
7 rows in set (0.00 sec)
```

- 示例 3：恢复表

```sql
--在实例 01907cb0-9b99-7714-8f1b-4b55c5eaxxxx 下执行
use db1;
CREATE TABLE t1(n1 int);
INSERT INTO t1 values(1);

mysql> SELECT * FROM t1;
+------+
| n1   |
+------+
|    1 |
+------+
1 row in set (0.00 sec)

create snapshot acc1_tab_snap1 for account acc1;--创建快照
truncate TABLE t1;--清空 t1

mysql> SELECT * FROM t1;
Empty set (0.01 sec)

restore account acc1 database db1 TABLE t1 FROM snapshot acc1_tab_snap1;--恢复快照

mysql> SELECT * FROM t1;--恢复成功
+------+
| n1   |
+------+
|    1 |
+------+
1 row in set (0.00 sec)
```

## 限制

- 目前只支持实例/数据库/表级别的恢复，暂不支持集群的。