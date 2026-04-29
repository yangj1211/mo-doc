# CREATE SNAPSHOT

`CREATE SNAPSHOT` creates a **read-only** point-in-time snapshot for a database, a table, or the cluster. Snapshots are used for time-travel queries, backup & restore, and data auditing.

## Syntax

```sql
CREATE SNAPSHOT <snapshot_name>
  FOR { DATABASE <db_name>
      | TABLE <db_name>.<tbl_name>
      | CLUSTER }
  [ COMMENT '<comment>' ];
```

## Parameters

| Parameter | Type | Required | Description |
|-----------|------|:--------:|-------------|
| `snapshot_name` | IDENTIFIER | Yes | Snapshot name, unique per account, ≤ 64 chars |
| `DATABASE` | KEYWORD | Exclusive | Snapshot a whole database |
| `TABLE` | KEYWORD | Exclusive | Snapshot a single table |
| `CLUSTER` | KEYWORD | Exclusive | Snapshot the whole cluster (only `sys` account) |
| `COMMENT` | STRING | No | Comment, up to 256 chars |

## Examples

### Example 1: snapshot a database

```sql
CREATE SNAPSHOT snap_demo_20260424
  FOR DATABASE demo
  COMMENT 'pre-release snapshot';
```

Output:

```text
Query OK, 1 row affected (0.03 sec)
```

### Example 2: snapshot a single table

```sql
CREATE SNAPSHOT snap_users_20260424
  FOR TABLE demo.users
  COMMENT 'daily backup';
```

Output:

```text
Query OK, 1 row affected (0.02 sec)
```

### Example 3: restore from a snapshot

After an accidental delete or update, you can restore the whole database from a prior snapshot:

```sql
RESTORE DATABASE demo FROM SNAPSHOT snap_demo_20260424;
```

Output:

```text
Query OK, 3 rows affected (0.08 sec)
```

:::{tip}
Restoring from a snapshot overwrites the current state of the database. For production, take a "pre-restore" snapshot first as a safety net.
:::

## Error codes

| Code | Meaning | Resolution |
|:----:|---------|------------|
| `20101` | Snapshot name already exists | Use a different name, or `DROP SNAPSHOT` first |
| `20102` | Target database or table not found | Check spelling and current database context |
| `20103` | Missing CREATE SNAPSHOT privilege | Grant via the `ACCOUNTADMIN` role |
| `20104` | `CLUSTER` level only allowed for sys account | Switch to the `sys` account |
| `20105` | Snapshot quota exceeded | Clean up old snapshots or ask admin for more |

## Related commands

- <a href="#"><code>DROP SNAPSHOT</code></a> — delete a snapshot
- <a href="#"><code>SHOW SNAPSHOTS</code></a> — list all snapshots in the current account
- <a href="#"><code>RESTORE FROM SNAPSHOT</code></a> — restore a database or table from a snapshot
- [`CREATE BRANCH`](../concepts/data-branch.md) — create a writable branch from a snapshot
