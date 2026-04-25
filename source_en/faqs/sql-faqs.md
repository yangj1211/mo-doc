# SQL FAQ

## Basic capability

**Is MatrixOne case-sensitive for identifiers?**

By default MatrixOne is case-insensitive for identifiers; case-sensitivity can be toggled via the `lower_case_table_names` parameter — see [Case-sensitivity support](../Reference/Variable/system-variables/lower_case_tables_name.md).

**Which SQL statements does MatrixOne support?**

See [SQL Statement Classification](../Reference/SQL-Reference/SQL-Type.md).

**Which data types does MatrixOne support?**

Common types are supported: integer, float, string, date/time, boolean, enum, binary, JSON. See [Data Types overview](../Reference/Data-Types/data-types.md).

**Which character sets does MatrixOne support?**

MatrixOne supports UTF-8 by default and only UTF-8.

**Which constraints and indexes does MatrixOne support?**

Primary Key, Unique Key, Not Null, Foreign Key, Auto Increment, and Secondary Index. Secondary indexes currently have syntax support only — no query acceleration.
MatrixOne also offers a sort key (`CLUSTER BY`) for tables without a primary key, which can pre-sort by columns you commonly query — accelerating those queries.

**Which query types does MatrixOne support?**

MatrixOne supports most common SQL queries:

Basic: group, distinct, filter, sort, limit, regex, etc.

Advanced: views, subqueries, joins, set operations, CTEs, window functions, prepared statements.

Aggregates: AVG, COUNT, MIN, MAX, SUM, etc.

System functions & operators: common string, date/time, math functions, and common operators.

**What are MatrixOne's reserved keywords?**

See [Keywords](../Reference/Language-Structure/keywords.md).

When a reserved keyword is used as an identifier, it must be wrapped in backticks — otherwise you get a syntax error. Non-reserved keywords can be used as identifiers without backticks.

**Does MatrixOne support materialized views?**

Not yet. With current AP performance, direct analytical queries usually work well. Materialized views are on the roadmap — if you have hard requirements please open an issue: <https://github.com/matrixorigin/matrixone/issues>.

**Does MatrixOne support Geometry?**

Not yet — but it's on the roadmap.

**Are MatrixOne functions and keywords case-sensitive?**

No. There's one exception: when you create a table or column wrapped in backticks, the name inside the backticks is case-sensitive. When querying, you need to wrap the name in backticks too.

**Does MatrixOne support transactions? What isolation levels?**

Yes — MatrixOne supports full ACID transactions, pessimistic and optimistic. Pessimistic is the default and uses Read Committed. Optimistic uses Snapshot Isolation.

## Data import / export

**How do I import data into MatrixOne?**

MatrixOne supports MySQL-style [`INSERT`](../Develop/import-data/insert-data.md) for real-time writes and [`LOAD DATA`](../Develop/import-data/bulk-load/bulk-load-overview.md) for offline bulk import.

**How do I export data from MatrixOne to a file?**

Use the [`mo-dump`](../Develop/export-data/modump.md) binary to dump to SQL or CSV, or [`SELECT INTO`](../Develop/export-data/select-into-outfile.md) to write CSV files.

**How do I dump only the table structure with `mo-dump`?**

Append `-no-data` to skip actual data.

**If the JSON object used with `LOAD DATA` is missing fields, will the load fail?**

If there are more JSON fields than table columns, import succeeds and the extra fields are ignored. If there are fewer fields, import fails.

**Can `source` commands use relative paths?**

Yes — relative to the current directory of the MySQL client. To avoid mistakes, prefer full paths. Also pay attention to file permissions.

**Importing a large file with `LOAD DATA` is slow. Any way to optimize?**

Set `PARALLEL` to `true` to enable parallel import. For example, for a 2 GB file, two threads can load in parallel — the second thread seeks to the 1 GB offset and reads forward. You can also pre-split the file yourself.

**Does `LOAD DATA` use transactions?**

All `LOAD` statements are transactional.

**Will triggers and stored procedures in a `source`-imported SQL file take effect?**

Currently, incompatible types / triggers / stored procedures must be hand-modified — otherwise the import errors out.

**Does `mo-dump` support batch export of multiple databases?**

Only single-database dumps are supported — run `mo-dump` multiple times for multiple databases.

**Does MatrixOne support importing from MinIO?**

Yes. `LOAD DATA` supports local files, S3 object storage, and S3-compatible object stores. MinIO is S3-protocol compatible, so it works. See [Import from local object storage](../Deploy/import-data-from-minio-to-mo.md).

**What do I do about garbled data due to encoding issues during import/export?**

Since MatrixOne only supports UTF-8 (not configurable), you can't fix garbling by changing the database/table charset. Instead, convert the source data to UTF-8. Common tools are `iconv` and `recode` — e.g., to convert GBK to UTF-8: `iconv -f GBK -t UTF8 t1.sql > t1_utf8.sql`.

**Which permissions are required for import / export?**

Tenant admins can import / export directly with the default role. Regular users need: `INSERT` on the target table for import; `SELECT` on the source table for `SELECT ... INTO OUTFILE`; for `mo-dump`, `SELECT` on all tables (`table.*`) and `SHOW TABLES` on all databases (`database.*`).

## Permissions

**Can a regular user be granted MOADMIN?**

No. `MOADMIN` is the top-level cluster-admin role and is held only by the root user.

## Other

**What is MatrixOne's `sql_mode`?**

Default is MySQL's `only_full_group_by` — in `SELECT`, every non-aggregate column must appear in `GROUP BY`. You can modify `sql_mode` to be more permissive.

**`SHOW TABLES` doesn't list temporary tables — how can I tell if a CREATE succeeded?**

Use `SHOW CREATE TABLE <temp_table>`. Temporary tables are visible only in the current session; when the session ends, the database automatically drops them and releases space — within the lifetime, you usually know manually.

**How do I check a query's execution plan?**

Use [`EXPLAIN`](../Reference/SQL-Reference/Other/Explain/explain.md) — it prints the plan.

```
EXPLAIN SELECT col1 FROM tbl1;
```

**How do I check the compression ratio of a table?**

Run a query like:

```sql
mysql> select ( sum(compress_size) + 1) / ( sum(origin_size) +1 ) from metadata_scan('db1.students', '*') m;
+---------------------------------------------------+
| (sum(compress_size) + 1) / (sum(origin_size) + 1) |
+---------------------------------------------------+
|                               0.44582681643679795 |
+---------------------------------------------------+
1 row in set (0.01 sec)
```

This means the `students` table compresses to roughly 44.96% of original size (~55.04% savings).

__NOTE__: During compression, data not yet flushed to disk may yield inaccurate ratios. Data is normally flushed within 5 minutes — query again after the flush completes for a reliable number.
