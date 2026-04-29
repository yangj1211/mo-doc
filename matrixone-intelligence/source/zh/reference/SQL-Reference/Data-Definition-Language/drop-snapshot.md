# DROP SNAPSHOT

## 语法说明

`DROP SNAPSHOT` 用于删除当前实例下创建的快照。

## 语法结构

```
> DROP SNAPSHOT snapshot_name;
```

## 示例

```sql
--在实例 585b49fc_852b_4bd1_b6d1_d64bc1d8xxxx 下执行
create snapshot sp1 for account `585b49fc_852b_4bd1_b6d1_d64bc1d8xxxx`;

mysql> show snapshots;
+---------------+-------------------------------+----------------+--------------------------------------+---------------+------------+
| SNAPSHOT_NAME | TIMESTAMP                     | SNAPSHOT_LEVEL | ACCOUNT_NAME                         | DATABASE_NAME | TABLE_NAME |
+---------------+-------------------------------+----------------+--------------------------------------+---------------+------------+
| sp1           | 2024-07-09 06:34:09.381035637 | account        | 585b49fc_852b_4bd1_b6d1_d64bc1d8xxxx |               |            |
+---------------+-------------------------------+----------------+--------------------------------------+---------------+------------+
1 row in set (0.16 sec)

drop snapshot sp1;

mysql>  show snapshots;
Empty set (0.01 sec)
```
