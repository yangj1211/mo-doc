# RESTORE ... FROM SNAPSHOT

## 语法说明

`RESTORE ... FROM SNAPSHOT` 用于从之前创建的租户级别的快照中进行租户/数据库/表级别的恢复数据。

## 语法结构

```
> RESTORE [[ACCOUNT <account_name>] [DATABASE database_name [TABLE table_name]]]FROM SNAPSHOT <snapshot_name> ;
```

## 示例

### 示例 1：恢复租户

```sql
--在实例 0193ba05-6cd6-7bca-ba0b-60828b25xxxx 下执行
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
7 rows in set (0.00 sec)

create snapshot A_snap1 for account `0193ba05-6cd6-7bca-ba0b-60828b25xxxx`;--创建快照
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
5 rows in set (0.01 sec)

restore account `0193ba05-6cd6-7bca-ba0b-60828b25xxxx` FROM snapshot A_snap1;--恢复租户级别快照

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

### 示例 2：恢复数据库

```sql
--在租户 acc1 下执行
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

create snapshot A_db_snap1 for account `0193ba05-6cd6-7bca-ba0b-60828b25xxxx`;--创建快照
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

restore account `0193ba05-6cd6-7bca-ba0b-60828b25xxxx` database db1 FROM snapshot A_db_snap1;--恢复数据库级别快照

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

### 示例 3：恢复表

```sql
--在租户 acc1 下执行
CREATE TABLE t1(n1 int);
INSERT INTO t1 values(1);

mysql> SELECT * FROM t1;
+------+
| n1   |
+------+
|    1 |
+------+
1 row in set (0.00 sec)

create snapshot A_tab_snap1 for account `0193ba05-6cd6-7bca-ba0b-60828b25xxxx`;--创建快照
truncate TABLE t1;--清空 t1

mysql> SELECT * FROM t1;
Empty set (0.01 sec)

restore account `0193ba05-6cd6-7bca-ba0b-60828b25xxxx` database db1 TABLE t1 FROM snapshot A_tab_snap1;--恢复快照

mysql> SELECT * FROM t1;--恢复成功
+------+
| n1   |
+------+
|    1 |
+------+
1 row in set (0.00 sec)
```
