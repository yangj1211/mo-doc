# **MySQL Compatibility**

This page compares the MySQL mode of MatrixOne Intelligence against native MySQL.

MatrixOne Intelligence is highly compatible with the MySQL 8.0 protocol, plus most of the commonly used MySQL 8.0 features and syntax. Common MySQL ecosystem tools — Navicat, MySQL Workbench, JDBC, and so on — also work. That said, because MatrixOne Intelligence has a different architecture and is still evolving, some features are not yet supported. This section walks through the differences with native MySQL across the following dimensions:

- DDL statements
- DCL statements
- DML statements
- Advanced SQL features
- Data types
- Indexes and constraints
- Partition support
- Functions and operators
- Storage engine
- Transactions
- Security and privileges
- Backup & restore
- System variables
- Programming languages
- Ecosystem tools

## DDL statements

### DATABASE

- Database / table names in Chinese characters are not supported.
- `ENCRYPTION` is parsed but has no effect.
- `ALTER DATABASE` is not supported.
- Only the `utf8mb4` character set with `utf8mb4_bin` collation is supported by default; this cannot be changed.

### TABLE

- `ENGINE=` in a table definition is silently ignored.
- The `ALTER TABLE` clauses `CHANGE [COLUMN]`, `MODIFY [COLUMN]`, `RENAME COLUMN`, `ADD [CONSTRAINT [symbol]] PRIMARY KEY`, `DROP PRIMARY KEY`, and `ALTER COLUMN ORDER BY` can be combined freely with each other but cannot be combined with other clauses.
- Temporary tables cannot be modified with `ALTER TABLE`.
- A table created with `CREATE TABLE ... CLUSTER BY ...` cannot be modified with `ALTER TABLE`.
- `ALTER TABLE` does not support `PARTITION` operations.
- `Cluster by column` is supported — pre-sorts a column to speed up queries.

### VIEW

- The `WITH CHECK OPTION` clause is not supported.
- The `DEFINER` and `SQL SECURITY` clauses are not supported.

### SEQUENCE

- MySQL does not support SEQUENCE objects. MatrixOne Intelligence does — `CREATE SEQUENCE` works with PostgreSQL-style syntax.
- `auto_increment` and `sequence` cannot be used together on the same column; combining them raises an error.

## DCL statements

### ACCOUNT

- Unlike the MatrixOne core, MatrixOne Intelligence has no separate ACCOUNT concept. Every instance you create within a region belongs to a single MatrixOne distributed cluster, and every instance is itself a separate ACCOUNT in the cluster — you cannot create another ACCOUNT inside an instance.

### Privileges

- `GRANT` semantics differ from MySQL.
- `REVOKE` semantics differ from MySQL.

### SHOW

- `SHOW` is not supported for `TRIGGER`, `FUNCTION`, `EVENT`, `PROCEDURE`, `ENGINE`, and similar objects.
- A few `SHOW` commands are accepted purely for syntactic compatibility and produce no output (e.g. `SHOW STATUS / PRIVILEGES`).
- Some commands have the same syntax as MySQL but behave differently because of the underlying architecture: `SHOW GRANTS`, `SHOW ERRORS`, `SHOW VARIABLES`, `SHOW PROCESSLIST`.
- MatrixOne Intelligence ships some additional `SHOW` commands for its own management: `SHOW BACKEND SERVERS`, `SHOW ACCOUNTS`, `SHOW ROLES`, `SHOW NODE LIST`, and so on.

### SET

- The system-variable surface differs significantly from MySQL. Most are accepted only for syntactic compatibility. Variables you can actually set today: `ROLE`, `SQL_MODE`, `TIME_ZONE`.

## DML statements

### SELECT

`SELECT ... FOR UPDATE` is currently single-table only.

### INSERT

- The `LOW_PRIORITY`, `DELAYED`, and `HIGH_PRIORITY` modifiers are not supported.

### UPDATE

- The `LOW_PRIORITY` and `IGNORE` modifiers are not supported.

### DELETE

- The `LOW_PRIORITY`, `QUICK`, and `IGNORE` modifiers are not supported.

### Subqueries

- `IN` with multi-level correlated subqueries is not supported.

### LOAD

- `SET` is supported but only in the form `SET column_name = nullif(expr1, expr2)`.
- `LOAD DATA LOCAL` works on the client side, but you must add `--local-infile` to your connection arguments.
- `JSONlines` import is supported via dedicated syntax.
- Loading from object storage is supported via dedicated syntax.

### EXPLAIN

- The output format of `Explain` and `Explain Analyze` follows PostgreSQL and differs significantly from MySQL.
- JSON output is not supported.

### Other

- `REPLACE` does not support a `VALUES row_constructor_list` form.

## Advanced SQL features

- Triggers are not supported.
- Stored procedures are not supported.
- The event scheduler is not supported.
- User-defined functions are not supported.
- Materialized views are not supported.

## Data types

- `BOOL`: unlike MySQL where boolean is really `int`, MatrixOne Intelligence has a true boolean type whose values can only be `true` or `false`.
- `DECIMAL`: in `DECIMAL(P, D)`, both the maximum precision `P` and the decimal scale `D` are 38 in MatrixOne Intelligence; MySQL allows up to 65 and 30 respectively.
- Floating point: MySQL deprecated `Float(M, D)` and `Double(M, D)` after 8.0.17, but MatrixOne Intelligence still supports them.
- `DATETIME`: MySQL ranges from `'1000-01-01 00:00:00'` to `'9999-12-31 23:59:59'`. MatrixOne Intelligence ranges from `'0001-01-01 00:00:00'` to `'9999-12-31 23:59:59'`.
- `TIMESTAMP`: MySQL ranges from `'1970-01-01 00:00:01.000000'` UTC to `'2038-01-19 03:14:07.999999'` UTC. MatrixOne Intelligence ranges from `'0001-01-01 00:00:00'` UTC to `'9999-12-31 23:59:59'` UTC.
- MatrixOne supports `UUID`.
- MatrixOne supports vector types.
- MatrixOne supports the `DATALINK` type.
- Spatial types are not supported.
- The `SET` type is not supported.
- The `MEDIUMINT` type is not supported.

## Indexes and constraints

- MatrixOne supports vector indexes.
- Secondary indexes are syntactically accepted but currently provide no actual speedup.
- Foreign keys do not support `ON CASCADE DELETE`.

## Partition support

- Six partition types are supported: `KEY`, `HASH`, `RANGE`, `RANGE COLUMNS`, `LIST`, `LIST COLUMNS`.
- Partition pruning works for `KEY` and `HASH`; the other four are not yet implemented.
- Subpartitions are syntactically accepted but not functional.
- `ADD / DROP / TRUNCATE PARTITION` is not yet supported.

## Functions and operators

### Aggregate functions

- A MatrixOne Intelligence-specific `Median` function is supported.

### CAST

- Type-conversion rules differ significantly from MySQL — see [CAST](../reference/Operators/operators/cast-functions-and-operators/cast.md).

### Window functions

- Only `RANK`, `DENSE_RANK`, and `ROW_NUMBER` are supported.

### JSON functions

- Supported: `JQ()`, `JSON_UNQUOTE`, `JSON_QUOTE`, `JSON_EXTRACT`, `JSON_EXTRACT_FLOAT64()`, `JSON_EXTRACT_STRING()`, `JSON_ROW()`, `TRY_JQ()`.

### System administration functions

- Supported: `CURRENT_ROLE_NAME()`, `CURRENT_ROLE()`, `CURRENT_USER_NAME()`, `CURRENT_USER`, `PURGE_LOG()`.

## Storage engine

- The TAE storage engine in MatrixOne Intelligence is fully developed in-house. MySQL engines such as InnoDB and MyISAM are not supported.
- TAE is the only storage engine; you don't need `ENGINE=XXX` to switch engines.

## Security and privileges

- Only `ALTER USER` is supported for changing passwords.
- Setting per-user connection limits is not supported.
- IP allowlists for connections are not supported.
- Authorization for `LOAD` from a file is not supported.
- `SELECT INTO` to a file is partially supported via `CREATE STAGE`.

## Transactions

- MatrixOne Intelligence defaults to pessimistic transactions.
- Unlike MySQL, DDL statements in MatrixOne Intelligence are transactional — DDL operations can be rolled back inside a transaction.
- Table-level `LOCK / UNLOCK TABLE` is not supported.

## Backup & restore

- Physical backup via `mobackup` is supported.
- Snapshot backup is supported.
- `mysqldump` is not supported; use `mo-dump` instead.
- `binlog` backup is not supported.

## System variables

- MatrixOne's `lower_case_table_names` has 2 modes; the default is 1.
- MatrixOne's `sql_mode` only supports `ONLY_FULL_GROUP_BY`.

## Programming languages

- The connectors and ORMs for Java, Python, C#, and Golang are largely supported. Connectors and ORMs for other languages may run into compatibility issues.

## Other tools

- Navicat, DBeaver, MySQL Workbench, and HeidiSQL mostly work, but the table-design feature is incomplete because of limited `ALTER TABLE` capabilities.
- The `xtrabackup` tool is not supported.
