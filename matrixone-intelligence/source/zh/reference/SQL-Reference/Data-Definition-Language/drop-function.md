# **DROP FUNCTION**

## **语法说明**

`DROP FUNCTION` 语句表示删除用户自定义函数。

## **语法结构**

```
> DROP FUNCTION <name> ([<arg_data_type> ]… )
```

## **示例**

**示例 1**

```sql
--删除有参函数

mysql> create function twosum (x float, y float) returns float language sql as 'select $1 + $2' ;
Query OK, 0 rows affected (0.02 sec)

mysql> drop function twosum(float,float);
Query OK, 0 rows affected (0.01 sec)

```

**示例 2**

```sql
--删除无参函数
mysql> CREATE FUNCTION t1_fun () RETURNS VARCHAR LANGUAGE SQL AS 'select n1 from t1 limit 1' ;
Query OK, 0 rows affected (0.01 sec)

mysql> drop function t1_fun();
Query OK, 0 rows affected (0.01 sec)

```