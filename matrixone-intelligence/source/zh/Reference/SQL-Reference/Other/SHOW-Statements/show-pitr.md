# SHOW PITR

## 语法说明

`SHOW PITR` 返回当前租户下创建的 PITR 的信息。

## 语法结构

```
> SHOW PITR[WHERE expr]
```

## 示例

```sql
create pitr account_pitr1 range 2 "h";
create pitr db_pitr1 for database db1 range 1 'y';
create pitr tab_pitr1 for database  db1 table t1 range 1 'y';

mysql> show pitr;
+-----------+---------------------+---------------------+------------+--------------------------------------+---------------+------------+-------------+-----------+
| PITR_NAME | CREATED_TIME        | MODIFIED_TIME       | PITR_LEVEL | ACCOUNT_NAME                         | DATABASE_NAME | TABLE_NAME | PITR_LENGTH | PITR_UNIT |
+-----------+---------------------+---------------------+------------+--------------------------------------+---------------+------------+-------------+-----------+
| tab_pitr  | 2024-12-17 03:19:38 | 2024-12-17 03:19:38 | table      | 0193ba05-6cd6-7bca-ba0b-60828b25xxxx | db1           | t1         |           1 | d         |
| db_pitr1  | 2024-12-17 03:19:02 | 2024-12-17 03:19:02 | database   | 0193ba05-6cd6-7bca-ba0b-60828b25xxxx | db1           | *          |           2 | d         |
| acc_pitr1 | 2024-12-17 03:17:27 | 2024-12-17 03:17:27 | account    | 0193ba05-6cd6-7bca-ba0b-60828b25xxxx | *             | *          |           1 | h         |
+-----------+---------------------+---------------------+------------+--------------------------------------+---------------+------------+-------------+-----------+
3 rows in set (0.17 sec)
```
