# DROP PITR

## 语法说明

`DROP PITR` 用于删除当前实例下创建的 pitr。

## 语法结构

```
> DROP PITR pitr_name;
```

## 示例

```sql
create pitr db_pitr1 for database db1 range 1 'y';

mysql> show pitr where pitr_name='db_pitr1';
+-----------+---------------------+---------------------+------------+--------------------------------------+---------------+------------+-------------+-----------+
| pitr_name | created_time        | modified_time       | pitr_level | account_name                         | database_name | table_name | pitr_length | pitr_unit |
+-----------+---------------------+---------------------+------------+--------------------------------------+---------------+------------+-------------+-----------+
| db_pitr1  | 2024-12-17 03:14:06 | 2024-12-17 03:14:06 | database   | 0193ba05-6cd6-7bca-ba0b-60828b25xxxx | db1           | *          |           1 | y         |
+-----------+---------------------+---------------------+------------+--------------------------------------+---------------+------------+-------------+-----------+
1 row in set (0.11 sec)

mysql> drop pitr db_pitr1;
Query OK, 0 rows affected (0.01 sec)

mysql> show pitr where pitr_name='db_pitr1';
Empty set (0.01 sec)
```
