# WAL

WAL (Write Ahead Log) is a technique tied to database atomicity and durability — converting random writes into sequential ones at commit time. Transaction changes scatter across pages; random writes are more expensive than sequential and degrade commit performance. WAL only records transaction changes — e.g., "a row added to a block". On commit, the new WAL entry is appended sequentially to the WAL file; dirty pages update asynchronously afterward and the corresponding WAL entries are destroyed to free space.

MatrixOne's WAL is a physical log — it records the location of each row update. Every replay produces the same data both logically and in underlying organization.

## Commit Pipeline

The Commit Pipeline processes transaction commits. Before committing, we update memtable and persist the WAL entry — the time those take determines commit performance. Persisting WAL involves IO and takes time. MatrixOne uses the Commit Pipeline to persist WAL asynchronously, not blocking in-memory updates.

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/architecture/wal_Commit_Pipeline.png)

**Commit flow:**

- Apply updates to memtable. Before entering the Commit Pipeline, transactions concurrently update memtable without blocking one another. These updates are in the uncommitted state — invisible to other transactions.

- Enter the Commit Pipeline for conflict checks.

- Persist WAL entries — collect them from memory and write to the backend. Persisting is asynchronous — the queue hands the entry to the backend and returns immediately, not waiting for write completion, so later transactions aren't blocked. The backend processes a batch of entries at once — Group Commit further accelerates persistence.

- Update memtable state to make the transaction visible — in the order transactions entered the queue. Visibility order matches WAL-entry write order.

## Checkpoint

Checkpoints write dirty data to storage, destroy old log entries, and free space. In MatrixOne, checkpoint is a background task:

- Pick a suitable timestamp — `t1` in the diagram — as the checkpoint. `t0` is the previous checkpoint. Dumps cover changes made in `[t0, t1]`.

- Dump DML changes. DML changes live in memtable blocks. Logtail Manager is an in-memory module that records which blocks each transaction changed. Scanning Logtail Manager for transactions in `[t0, t1]`, we start background transactions to dump these blocks to storage and record their addresses in metadata. That way, DML changes committed before `t1` can be located via metadata. To keep checkpoints frequent and WAL bounded, even blocks with just a single-row change are dumped.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/architecture/wal_Checkpoint1.png width=80% heigth=80%/>
</div>

- Scan the Catalog to dump DDL and metadata changes. Catalog is a tree containing DDL and metadata — each node records the timestamp of the change. Scanning collects all changes within `[t0, t1]`.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/architecture/wal_Checkpoint2.png width=80% heigth=80%/>
</div>

- Destroy old WAL entries. Logtail Manager records each transaction's LSN. Based on timestamp, we find the last transaction before `t1` and ask the Log Backend to delete all logs up to that transaction's LSN.

## Log Backend

MatrixOne's WAL can sit on different Log Backends. The initial backend was the local filesystem. For distributed support, we built the high-reliability, low-latency Log Service as a new backend. To adapt across log backends, we abstract a virtual backend — lightweight drivers adapt different backends.

**Required driver APIs:**

- Append — async write on commit:

```
Append(entry) (Lsn, error)
```

- Read — batch read on restart:

```
Read(Lsn, maxSize) (entry, Lsn, error)
```

- Truncate — destroy all entries before an LSN to free space:

```
Truncate(lsn Lsn) error
```

## Group Commit

Group Commit accelerates log-entry persistence. Persistence involves IO and can bottleneck commits. To reduce latency, batch entries to the Log Backend. For filesystems, `fsync` is expensive — `fsync`-per-entry kills throughput. Filesystem-backed Log Backend does a single `fsync` for a batch of entries — total flush time is close to single-entry flush time.

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/architecture/wal_Group_Commit.png)

Log Service supports concurrent writes — individual entry flush times overlap — shortening total write time and raising commit concurrency.

## Handling out-of-order LSNs in the Log Backend

Concurrent writes mean writes don't complete in submission order — Log Backend LSNs diverge from the logical LSNs we assigned. Truncate and restart must handle this. To keep Log Backend LSNs mostly ordered — keeping out-of-order span small — we maintain a logical LSN window: if an early log entry is still in-flight, new entries stop being written. E.g., with window length 7 in the diagram, an in-flight LSN 13 blocks entries with LSN ≥ 20.

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/architecture/wal_Log_Backend.png)

Truncate in Log Backend destroys all entries before a given LSN. The logical LSNs of entries before that physical LSN must be ≤ the logical truncate point. Example: truncate logical at 7 — the entry sits at Log Backend position 11, but Log Backend entries 5, 6, 7, 10 correspond to logical LSNs > 7 and can't be truncated. The Log Backend can only truncate up to 4.

On restart, we skip discontiguous entries at the start and end. E.g., the Log Backend wrote up to 14 when the machine crashed; on restart, based on the last truncate info, 8, 9, 11 are filtered out at the start. After reading everything, 6 and 14 are discontiguous — we drop them at the end.

## WAL format in MatrixOne

Each write transaction maps to one log entry — LSN, Transaction Context, and multiple Commands.

```
+---------------------------------------------------------+
|                  Transaction Entry                      |
+-----+---------------------+-----------+-----------+-   -+
| LSN | Transaction Context | Command-1 | Command-2 | ... |
+-----+---------------------+-----------+-----------+-   -+
```

**LSN**: per log entry. Monotonically increasing; used for entry deletion at checkpoint.

**Transaction Context**: transaction info

- `StartTS`: transaction start timestamp.
- `CommitTS`: transaction end timestamp.
- `Memo`: which places data was changed. On restart, this gets restored into the Logtail Manager — needed for checkpoint.

```
+---------------------------+
|   Transaction Context     |
+---------+----------+------+
| StartTS | CommitTS | Memo |
+---------+----------+------+
```

**Transaction Commands**: each write in a transaction maps to one or more commands. A log entry records every command in the transaction.

| Operator | Command |
| :--- | :--- |
| DDL | Update Catalog |
| Insert | Update Catalog |
|  | Append |
| Delete | Delete |
| Compact & Merge | Update Catalog |

- Operators: in MatrixOne, DN handles commit, writes log entries, and runs checkpoints. DN supports create/drop database, create/drop table, alter table, insert, delete, plus background sort. Update is split into insert + delete.

    - **DDL**
    DDL covers create/drop database, create/drop table, and alter table. DN records table/database info in the Catalog. The in-memory Catalog is a tree; each node is a catalog entry. Four kinds of catalog entries: database, table, segment, block. Segments and blocks are metadata, changing on insert and background sort. Each database entry corresponds to a database, each table entry to a table. Every DDL operation corresponds to a database/table entry, recorded in the entry as an Update Catalog Command.

    - **Insert**
    New inserts are recorded in the Append Command. DN data lives in blocks; multiple blocks form a segment. If DN doesn't have enough blocks or segments to hold new inserts, more are created — those changes are recorded in Update Catalog Commands. In large transactions, CN writes directly to S3, DN only commits metadata — so Append Command data stays small.

    - **Delete**
    DN records row numbers where Delete occurred. On read, we read all inserted data and subtract those rows. In a transaction, all deletes on the same block are merged into one Delete Command.

    - **Compact & Merge**
    DN launches background transactions to dump in-memory data to S3 and sort S3 data by primary key for easier read-time filtering. Compact happens on a single block — resulting data inside the block is sorted. Merge happens inside a segment (across multiple blocks); the entire segment becomes sorted. Data before and after is identical — only metadata changes: old blocks/segments are deleted and new ones created. Each delete/create corresponds to an Update Catalog Command.

- Commands

<div>&nbsp&nbsp&nbsp1. &nbspUpdate Catalog</div>

Catalog top-down: database, table, segment, block. One Update Catalog Command maps to one Catalog Entry. Every DDL or metadata update produces one Update Catalog Command. Update Catalog Command contains Dest and EntryNode.

```
+-------------------+
|   Update Catalog  |
+-------+-----------+
| Dest  | EntryNode |
+-------+-----------+
```

Dest is where this command applies — it records the node and its ancestor IDs. On restart, Dest locates the operation on the Catalog.

| Type | Dest |
| :--- | :--- |
| Update Database | database id |
| Update Table | database id, table id |
| Update Segment | database id, table id, segment id |
| Update Block | database id, table id, segment id, block id |

EntryNode records the entry's create and delete times. If the entry isn't deleted, delete time is 0. If the current transaction is creating or deleting, the corresponding timestamp is `UncommitTS`.

```
+-------------------+
|    Entry Node     |
+---------+---------+
| Create@ | Delete@ |
+---------+---------+
```

For segments and blocks, Entry Node also records `metaLoc` and `deltaLoc` — the S3 addresses of data and delete records.

```
 +----------------------------------------+
 |               Entry Node               |
 +---------+---------+---------+----------+
 | Create@ | Delete@ | metaLoc | deltaLoc |
 +---------+---------+---------+----------+
```

For tables, Entry Node also records the table schema.

```
 +----------------------------+
 |         Entry Node         |
 +---------+---------+--------+
 | Create@ | Delete@ | schema |
 +---------+---------+--------+
```

<div>&nbsp&nbsp&nbsp2. &nbspAppend</div>

Append Command records inserted data and its location.

```
+-------------------------------------------+
|             Append Command                |
+--------------+--------------+-   -+-------+
| AppendInfo-1 | AppendInfo-2 | ... | Batch |
+--------------+--------------+-   -+-------+
```

- Batch: the data being inserted.

- AppendInfo: data in an Append Data Command may span multiple blocks. Each block has one AppendInfo — pointer to data (offset + length in the Command's Batch) plus destination (database id, table id, segment id, block id, offset, length in the block).

```
+------------------------------------------------------------------------------+
|                              AppendInfo                                      |
+-----------------+------------------------------------------------------------+
| pointer to data |                     destination                            |
+--------+--------+-------+----------+------------+----------+--------+--------+
| offset | length | db id | table id | segment id | block id | offset | length |
+--------+--------+-------+----------+------------+----------+--------+--------+
```

<div>&nbsp&nbsp&nbsp3. &nbspDelete Command</div>

Each Delete Command contains deletes on one block only.

```
+---------------------------+
|      Delete Command       |
+-------------+-------------+
| Destination | Delete Mask |
+-------------+-------------+
```

- Destination: which block the delete happened on.
- Delete Mask: the row numbers deleted.
