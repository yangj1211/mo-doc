# MySQL Compatibility

This article compares MatrixOne's MySQL mode against native MySQL.

MatrixOne is highly compatible with MySQL 8.0 — wire protocol, common features, and syntax. MatrixOne also supports common MySQL ecosystem tools — Navicat, MySQL Workbench, JDBC, etc. Because MatrixOne's architecture is different, and it's still evolving, some features are not yet supported. This article details MatrixOne vs. native MySQL across:

- DDL
- DCL
- DML
- Advanced SQL
- Data types
- Indexes and constraints
- Partitioning
- Functions and operators
- Storage engines
- Transactions
- Security and privileges
- Backup and restore
- System variables
- Programming languages
- Ecosystem tools

## DDL

### DATABASE

* Chinese-character table names aren't supported.
* `ENCRYPTION` is parsed but not active.
* `ALTER DATABASE` is not supported.
* Only `utf8mb4` charset and `utf8mb4_bin` collation are supported — not configurable.

### TABLE

* `ENGINE=` in table definitions isn't supported — MatrixOne silently ignores it.
* These `ALTER TABLE` clauses can be freely combined: `CHANGE [COLUMN]`, `MODIFY [COLUMN]`, `RENAME COLUMN`, `ADD [CONSTRAINT [symbol]] PRIMARY KEY`, `DROP PRIMARY KEY`, and `ALTER COLUMN ORDER BY`. They don't combine with other clauses.
* Temporary tables don't support `ALTER TABLE`.
* Tables created with `CREATE TABLE ... CLUSTER BY ...` don't support `ALTER TABLE`.
* `ALTER TABLE` doesn't support partition operations.
* `CLUSTER BY column` is supported for pre-sorting to accelerate queries.

### VIEW

* `WITH CHECK OPTION` is not supported.
* `DEFINER` and `SQL SECURITY` clauses are not supported.

### SEQUENCE

* MySQL lacks a `SEQUENCE` object; MatrixOne supports `CREATE SEQUENCE` — syntax matches PostgreSQL.
* When using `SEQUENCE` in tables, `auto_increment` and `sequence` can't be combined — that errors.

## DCL

### ACCOUNT

* Multi-tenant `ACCOUNT` is unique to MatrixOne — including `CREATE/ALTER/DROP ACCOUNT`.

### Privileges

* `GRANT` — authorization logic differs from MySQL.
* `REVOKE` — revoke logic differs from MySQL.

### SHOW

* Some `SHOW` targets aren't supported: `TRIGGER`, `FUNCTION`, `EVENT`, `PROCEDURE`, `ENGINE`, etc.
* Some `SHOW` commands exist only for syntax compatibility and produce no output — `SHOW STATUS/PRIVILEGES` etc.
* Some commands have the same syntax as MySQL but different semantics — `SHOW GRANTS`, `SHOW ERRORS`, `SHOW VARIABLES`, `SHOW PROCESSLIST`.
* MatrixOne-specific `SHOW` commands include `SHOW BACKEND SERVERS`, `SHOW ACCOUNTS`, `SHOW ROLES`, `SHOW NODE LIST`, etc.

### SET

* MatrixOne's system variables differ significantly from MySQL — most exist for syntax compatibility. The ones currently settable are `ROLE`, `SQL_MODE`, `TIME_ZONE`.

## DML

### SELECT

`SELECT ... FOR UPDATE` currently only supports single-table queries.

### INSERT

* Modifiers `LOW_PRIORITY`, `DELAYED`, `HIGH_PRIORITY` aren't supported.

### UPDATE

* `LOW_PRIORITY` and `IGNORE` modifiers aren't supported.

### DELETE

* `LOW_PRIORITY`, `QUICK`, `IGNORE` modifiers aren't supported.

### Subqueries

* Multi-level correlated `IN` subqueries aren't supported.

### LOAD

* `SET` is supported but only in the form `SET columns_name = nullif(expr1, expr2)`.
* `LOAD DATA LOCAL` from the client is supported — the `--local-infile` flag is required at connection time.
* JSONlines import is supported via specific syntax.
* Import from object storage is supported via specific syntax.

### EXPLAIN

* `EXPLAIN` and `EXPLAIN ANALYZE` formats follow PostgreSQL, differing significantly from MySQL.
* JSON-format output isn't supported.

### Other

* `REPLACE` doesn't support a `VALUES row_constructor_list` with multiple rows.

## Advanced SQL

* Triggers aren't supported.
* Stored procedures aren't supported.
* Event scheduler isn't supported.
* Materialized views aren't supported.
* UDFs — Python only. Usage differs significantly from MySQL.

## Stream computing

* Unique to MatrixOne. v24.2.0.1 supports only the Kafka connector.
* Kafka connector creation and use require specific syntax.

## Data types

* BOOL: unlike MySQL (where BOOL is actually `int`), MatrixOne's BOOL is a distinct type — only `true` or `false`.
* DECIMAL: MatrixOne `DECIMAL(P, D)` supports up to 38 significant digits and 38 after the decimal point; MySQL supports 65 and 30.
* Floats: MySQL 8.0.17+ deprecated `Float(M, D)` and `Double(M, D)`; MatrixOne retains them.
* DATETIME: MySQL's max range is `'1000-01-01 00:00:00'` to `'9999-12-31 23:59:59'`; MatrixOne's is `'0001-01-01 00:00:00'` to `'9999-12-31 23:59:59'`.
* TIMESTAMP: MySQL max is `'1970-01-01 00:00:01.000000'` UTC to `'2038-01-19 03:14:07.999999'` UTC; MatrixOne max is `'0001-01-01 00:00:00'` UTC to `'9999-12-31 23:59:59'` UTC.
* UUID is supported.
* VECTOR is supported.
* DATALINK is supported.
* Spatial types are not supported.
* SET type is not supported.
* MEDIUMINT is not supported.

## Indexes and constraints

* Vector indexes are supported.
* Secondary indexes don't currently accelerate `IN`, `BETWEEN AND`, or `LIKE`.
* Foreign keys don't support `ON CASCADE DELETE`.

## Partitioning

* `KEY`, `HASH`, `RANGE`, `RANGE COLUMNS`, `LIST`, `LIST COLUMNS` partition types are supported.
* `KEY` and `HASH` partition pruning are supported; the other four aren't yet.
* Subpartitions are parsed but not functional.
* `ADD / DROP / TRUNCATE PARTITION` aren't supported yet.

## Keywords

* MatrixOne and MySQL keyword lists differ significantly — see [MatrixOne keywords](../../Reference/Language-Structure/keywords.md).

## Functions and operators

### Aggregates

* MatrixOne-specific `Median` function is supported.

### CAST

* Type-conversion rules differ significantly from MySQL — see [CAST](../../Reference/Operators/operators/cast-functions-and-operators/cast.md).

### Window functions

* Only `RANK`, `DENSE_RANK`, `ROW_NUMBER`.

### JSON

* Only `JSON_UNQUOTE`, `JSON_QUOTE`, `JSON_EXTRACT`.

### System management

- `CURRENT_ROLE_NAME()`, `CURRENT_ROLE()`, `CURRENT_USER_NAME()`, `CURRENT_USER`, `PURGE_LOG()` are supported.

## Storage engines

* MatrixOne's TAE engine is entirely in-house — InnoDB, MyISAM, etc. aren't supported.
* TAE is the only storage engine; `ENGINE=XXX` isn't needed.

## Security and privileges

* Only `ALTER USER` can change passwords.
* The max number of connections per user isn't configurable.
* Connection IP allow-lists aren't supported.
* File-level `LOAD` authorization isn't supported.
* File-level `SELECT INTO` authorization is partially supported via `CREATE STAGE`.

## Transactions

* MatrixOne defaults to pessimistic transactions.
* Unlike MySQL, DDL in MatrixOne is transactional — DDL can roll back within a transaction.
* `SET` operations aren't allowed within a transaction.
* Table-level locking `LOCK / UNLOCK TABLE` isn't supported.

## Backup and restore

* Physical backup via `mobackup` is supported.
* Snapshot backup is supported.
* `mysqldump` isn't supported — use `mo-dump`.
* Binlog-based backup isn't supported.

## System variables

* `lower_case_table_names` has two modes in MatrixOne; default is 1.
* `sql_mode` supports only `ONLY_FULL_GROUP_BY`.

## System tables

* MatrixOne has both its own system tables and compatibility-oriented MySQL-style ones.
* `mysql` and `information_schema` are compatible with MySQL usage.
* `system_metrics` captures runtime state / monitoring metrics.
* `system` holds user and system log records.
* `mo_catalog` holds database objects and metadata.

## Programming languages

* Java, Python, C#, Go connectors and ORMs work — others may have compatibility issues.

## Ecosystem tools

* Navicat, DBeaver, MySQL Workbench, HeidiSQL generally work, though table-design features are limited because `ALTER TABLE` is incomplete.
* `xtrabackup` isn't supported.
