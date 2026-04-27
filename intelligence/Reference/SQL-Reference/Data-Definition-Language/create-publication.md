# **CREATE PUBLICATION**

## **语法说明**

`CREATE PUBLICATION` 将一个新的发布添加到当前数据库中。

## **语法结构**

```
CREATE PUBLICATION pubname
    DATABASE database_name ACCOUNT
    [ { ALL
    | account_name, [, ... ] }]
    [ COMMENT 'string']
```

## 语法解释

- pubname：发布名称。发布名称必须与当前数据库中任何现有发布的名称不同。
- database_name：当前租户下已存在的某个数据库名称。
- account_name：可获取该发布的租户名称。

## **示例**

1. **发布者**: 实例 A 创建数据库 mall 与表 customer 并发布此数据库为 pub_mall:

    ```sql
    -- 实例 A
    create database mall;
    CREATE TABLE mall.customer (
    customer_id INT,
    customer_name VARCHAR(255)
    );
    create publication pub_mall database mall;

    mysql> show publications;
    +-------------+----------+---------------------+-------------+-------------+----------+
    | publication | database | create_time         | update_time | sub_account | comments |
    +-------------+----------+---------------------+-------------+-------------+----------+
    | pub_mall    | mall     | 2024-05-27 09:02:49 | NULL        | *           |          |
    +-------------+----------+---------------------+-------------+-------------+----------+

    1 row in set (0.17 sec)
    ```

2. **订阅者**: 实例 B 和实例 C 都创建订阅库 sub_mall（订阅自实例 A 的 pub_mall），于是得到实例 A 数据库 mall 中的所有数据：

    ```sql
    -- 实例 B && 实例 C 
    create database sub_mall from 018fb8d3_2b05_7be8_b526_bb62576dxxxx publication pub_mall;
    use sub_mall;

    mysql> show subscriptions;
    +----------+--------------------------------------+--------------+---------------------+----------+---------------------+
    | pub_name | pub_account                          | pub_database | pub_time            | sub_name | sub_time            |
    +----------+--------------------------------------+--------------+---------------------+----------+---------------------+
    | pub_mall | 018fb8d3_2b05_7be8_b526_bb62576dxxxx | mall         | 2024-05-27 09:02:49 | sub_mall | 2024-05-27 09:05:44 |
    +----------+--------------------------------------+--------------+---------------------+----------+---------------------+
    1 row in set (0.08 sec)

    mysql> show tables;
    +--------------------+
    | Tables_in_sub_mall |
    +--------------------+
    | customer           |
    +--------------------+
    ```

:::{note}
如果需要取消订阅，可以直接删除已订阅的数据库名称，使用 [`DROP DATABASE`](drop-database.md)。
:::