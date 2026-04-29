# **SQL FAQs**

* **Which database is MatrixOne compatible with?**

MatrixOne is highly compatible with MySQL 8.0 — SQL syntax, wire protocol, operators and functions, and so on. For the full list of differences, see the [MySQL compatibility list](../../overview/mysql-compatibility.md).

* **Which SQL statements does MatrixOne support?**

For the full list of SQL statements MatrixOne supports today, see [this reference](../../reference/SQL-Reference/SQL-Type.md).

* **Which data types does MatrixOne support?**

MatrixOne currently supports the common integer, floating-point, string, datetime, boolean, enum, binary, and JSON types. See [the reference](../../reference/Data-Types/data-types.md) for the full list.

* **Which character sets does MatrixOne support?**

MatrixOne uses UTF-8 by default and currently supports only UTF-8.

* **Which constraints and indexes does MatrixOne support?**

MatrixOne supports primary key, unique key, NOT NULL, foreign key, auto-increment, and secondary indexes. Secondary indexes are syntactically accepted but currently provide no actual speedup.
MatrixOne also offers a sort key (`Cluster by`) for tables without a primary key, which pre-sorts on the column you query the most to speed it up.

* **Which kinds of queries does MatrixOne support?**

MatrixOne supports most common SQL queries:

Basic: grouping, deduplication, filtering, sorting, limiting, regular expressions, and other basics.

Advanced: views, subqueries, joins, set operations, common table expressions (CTEs), window functions, and prepared statements.

Aggregate functions: common aggregates such as `AVG`, `COUNT`, `MIN`, `MAX`, `SUM`.

System functions and operators: common string, datetime, mathematical functions, and the usual operators.

* **Which keywords are reserved in MatrixOne?**

For the full list of reserved keywords, see [this reference](../../reference/Language-Structure/keywords.md).

To use a reserved keyword as an identifier, wrap it in backticks; otherwise the parser raises an error. Non-reserved keywords can be used as identifiers without backticks.

* **Are functions and keywords case-sensitive in MatrixOne?**

No.

There is exactly one case where MatrixOne cares about case: if you create a table or column with a name wrapped in backticks (`` ` ``), the case inside the backticks matters. To query that table or column, you must wrap the name in backticks again.

* **How do I import data into MatrixOne Intelligence?**

MatrixOne supports the same [`INSERT`](../../workspace/sql/data-rw/import-data/insert-data.md) statement as MySQL for real-time inserts, and [`LOAD DATA`](../../workspace/sql/data-rw/import-data/bulk-load/bulk-load-overview.md) for offline bulk loading.

In MatrixOne Intelligence, you can also use the [Import Data](../../workspace/sql/data-rw/import-data/bulk-load/load-s3.md) feature in the UI to load `csv` or `jsonline` files from object storage offline. You can also use publish/subscribe to quickly bring in data already stored in another instance.

* **How do I export data from MatrixOne Intelligence to a file?**

In MatrixOne Intelligence, use the [`mo-dump`](../../workspace/tools/modump.md) binary to export data as SQL or CSV.

* **Does MatrixOne support transactions? What isolation levels does it support?**

MatrixOne supports ACID transactions (atomicity, consistency, isolation, durability) and offers both pessimistic and optimistic transactions, with pessimistic as the default. Pessimistic transactions use Read Committed; optimistic transactions use Snapshot Isolation.

* **What is `sql_mode` in MatrixOne?**

  MatrixOne defaults `sql_mode` to MySQL's `only_full_group_by`. By default, every column in a `SELECT` (other than columns inside aggregates) must appear in the `GROUP BY`. You can change `sql_mode` if you need to allow non-strict `GROUP BY`.

* **How do I look at the execution plan for my query?**

  To see how MatrixOne executes a query, use [`EXPLAIN`](../../reference/SQL-Reference/Other/Explain/explain.md) — it prints the query plan.

  ```
  EXPLAIN SELECT col1 FROM tbl1;
  ```

  You can also see a graphical execution plan in the [Query Analysis](../../workspace/data/explore/query-anlysis/query_profile.md) module of the MatrixOne Intelligence database management console.
