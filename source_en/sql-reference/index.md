# SQL Reference

{.mo-subtitle}
MatrixOne SQL syntax reference. This section is organized by command type — DDL, DML, admin commands, functions, and operators.

This demo ships `CREATE SNAPSHOT` as the sample page; the full content needs to be migrated from the official SQL Reference by engineering (a few days of work).

## Browse by command type

| Category | Description | Examples |
|----------|-------------|----------|
| DDL | Data definition — database / table / view / index | CREATE / DROP / ALTER TABLE, CREATE VIEW... |
| DML | Data manipulation — CRUD, bulk load | INSERT, UPDATE, DELETE, LOAD DATA... |
| **Admin commands** | Snapshot, PITR, backup, tenant, privileges | [CREATE SNAPSHOT](snapshot.md), CREATE PITR... |
| Functions & operators | Aggregate, string, date, JSON, vector | COUNT, DATE_FORMAT, JSON_EXTRACT... |
| System variables | Config, runtime parameters | sql_mode, time_zone... |

```{toctree}
:maxdepth: 1
:caption: Admin commands

snapshot
```
