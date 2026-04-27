# TAE Storage Engine

MatrixOne's storage engine is called TAE — Transactional Analytical Engine.

## Storage-engine architecture

TAE's smallest IO unit is a Column Block — currently fixed-row-count organized, with special handling for Blob columns.

TAE organizes data per-table as an LSM (Log-Structured Merge) tree. The current TAE is a three-tier LSM: L0, L1, L2. L0 is small and lives in memory; L1 and L2 are persisted to disk.

In TAE, L0 consists of Transient Blocks — data is not sorted there. L1 consists of Sorted Blocks containing sorted data. New data is always inserted into the newest Transient Block. When a block's row count exceeds the limit, it's primary-key-sorted and flushed to L1 as a Sorted Block. When the number of Sorted Blocks exceeds a segment limit, Merge Sort by primary key produces L2.

Both L1 and L2 hold data sorted by primary key. The difference: L1 ensures data inside each block is sorted by PK; L2 ensures data inside each segment is sorted by PK. A segment is a logical concept equivalent to a Row Group or Row Set in other implementations. Based on update (delete) activity, a segment can be compacted into a new segment; segments can also be merged into a new segment. Background async tasks drive these operations — scheduling trades off write amplification and read amplification.

## Features

- **AP-friendly**: efficient compression, high query efficiency, fast aggregates, strong concurrency — better performance and scalability on large data, more appropriate for analytical and warehousing use cases.
- **Flexible workload fit**: via the Column Family concept, you can adapt to workloads. If all columns are in one Column Family (all column data stored together), it looks like a HEAP file — row-store-like behavior. If each column is its own Column Family, it's column-store-like. DDL choice is all it takes to switch — no changes to the underlying engine.

## Indexes and metadata

Like traditional column stores, TAE adds Zonemap (min/max) info at block and segment levels. As a TP-capable engine, TAE implements full PK constraints — multi-column PKs and global auto-increment IDs. A PK index is created by default per table, used for dedup on insert (to satisfy PK constraints) and filtering by PK.

PK dedup is critical on insert; TAE balances three factors:

- Query performance
- Memory usage
- Data-layout fit

By granularity, TAE indexes split into table-level and segment-level. A table-level index might be one per table, while segment-level has one per segment. Because TAE tables consist of many segments, each passing through L1→L3 compaction/merge (unsorted → sorted), table-level indexes are less friendly. TAE indexes are therefore built at segment level.

Segment-level indexes come in two variants: appendable and non-appendable. For non-appendable segments, the index is a two-level structure with Bloom filter + Zonemap. For appendable segments (at least one appendable block plus multiple non-appendable ones), the appendable-block index is an in-memory Adaptive Radix Tree (ART) + Zonemap; non-appendable blocks have Bloom filter + Zonemap.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/Tae/index-metadata.png width=80% heigth=80%/>
</div>

## Buffer management

In a stable storage engine, fine-grained memory management requires a buffer manager. In theory it's just an LRU cache — but databases don't directly use OS page cache, especially for TP-style workloads.

MatrixOne uses a buffer manager. Each buffer node has a fixed size, allocated to one of four areas:

1. Mutable: fixed-size buffer for L0 Transient Column Blocks.
2. SST: L1 and L2 blocks.
3. Index: index information.
4. Redo log: uncommitted transaction data — each transaction needs at least one buffer.

Each node is either Loaded or Unloaded. When a user pins a node via the buffer manager: if Loaded, refcount increments; if Unloaded, it's read from disk or remote storage, then refcount increments. Under memory pressure, the system evicts nodes by LRU to free space. On Unpin, the handle is closed. If refcount reaches 0, the node becomes a candidate for eviction; with refcount > 0, it stays.

## WAL and log replay

TAE optimizes redo log processing so column-store WAL is more efficient. Compared to row stores, TAE only records redo log at commit time, not per write. The buffer manager reduces IO — especially for short-lived rollback-capable transactions — avoiding IO events. TAE also supports large / long transactions.

TAE's WAL uses the following log-entry header format:

| Field | Bytes |
|---|---|
| GroupID | 4 |
| LSN | 8 |
| Length | 8 |
| Type | 1 |

Transaction log-entry types:

| Type | Code | Value | Description |
|---|---|---|---|
| AC | int8 | 0x10 | Complete write of a committed transaction |
| PC | int8 | 0x11 | Partial write of a committed transaction |
| UC | int8 | 0x12 | Partial write of an uncommitted transaction |
| RB | int8 | 0x13 | Transaction rollback |
| CKP | int8 | 0x40 | Checkpoint |

Most transactions have one log entry, but larger or longer ones may need multiple. A transaction's log may include one or more UC entries plus a PC entry, or just one AC entry. UC entries go into a dedicated group.

In TAE, log-entry payloads contain multiple transaction nodes — including DML deletes / appends / updates and DDL such as create / drop table and database. Each transaction node is a subitem of a committed log entry — think of it as a piece of the log. Active-transaction nodes share a fixed-size memory region managed by the buffer manager. When space runs low, some nodes are unloaded and their corresponding entries are written to the redo log. On load, those entries are replayed — applied to the corresponding transaction nodes.

Checkpoint is a safe point — during restart, the state machine starts applying log entries from here. Entries before the checkpoint are no longer needed and are physically destroyed at the right time. TAE records the last checkpoint via a group, so replay after restart can start there.

TAE's WAL and log-replay logic is abstracted into a module called logstore. It abstracts underlying log access — implementations range from standalone to distributed. Physically, logstore behaves like a message queue. Starting with MatrixOne 0.6, we evolved into a cloud-native version using an independent shared-log service. In future versions, TAE's logstore will be adjusted to access this external shared-log service directly — without relying on local storage.

## Transaction processing

TAE uses MVCC (Multi-Version Concurrency Control) for isolation. Each transaction has a consistent read view determined by its start timestamp — reads inside the transaction never reflect concurrent modifications. TAE offers fine-grained optimistic concurrency — conflicts only arise when two transactions update the same row and column. Reads don't take locks; they use the version existing at transaction start. When two transactions update the same value, the second fails with a write-write conflict.

In TAE, a table consists of multiple segments — each segment is the result of many transactions. A segment can be represented `$[T{start}, T{end}]$` — `$T{start}$` is the earliest committer's commit time, `$T{end}$` is the latest committer's commit time. To support compaction and merging, we add a dimension to distinguish versions: `$([T{start} T{end}], [T{create}, T{drop}])$`. `$T{create}$` is the segment's creation time; `$T{drop}$` is the drop time. `$T{drop} = 0$` means the segment isn't dropped. Blocks are represented the same way. On commit, we get the read view: `$(Txn{commit} \geqslant T{create})\bigcap((T{drop}=0)\bigcup(T{drop} > Txn{commit}))$`.

Segment generation and evolution is done by background async tasks. To keep reads consistent, TAE integrates these tasks into the transaction framework, as shown:

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/Tae/segment.png?raw=true)

L0 block `$Block1{L0}$` is created at `$t1$` containing data from `$Txn1, Txn2, Txn3, Txn4$`. `$Block1{L0}$` starts sorting at `$t11$`; its read view is the baseline plus an uncommitted update node. Sorting and persisting may take a while. Before committing the sorted `$Block2{L1}$`, there are two committed transactions `$Txn5, Txn6$` and one uncommitted `$Txn7$`. If `$Txn7$` commits at `$t16$`, it fails because `$Block1{L0}$` was terminated. Update nodes committed in `$(t11, t16)$` — `$Txn5, Txn6$` — are merged into a new update node that commits with `$Block2{L1}$` at `$t16$`.

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/Tae/compaction.png?raw=true)

Compaction terminates a batch of blocks or segments and atomically creates a new block or segment (or index). Compared to normal transactions, this takes longer — we don't want to block update / delete transactions on involved blocks or segments. So we extend the read view to include block and segment metadata. On committing a normal transaction, if the metadata of a written block (or segment) has changed (committed), the transaction fails. For compaction transactions, the writes are soft-drop plus add. During execution, each write checks for write-write conflicts — on conflict, the transaction aborts early.

## MVCC

A database's version-storage mechanism determines how different tuple versions are stored and what each version carries. TAE creates a lock-free version chain based on the data-tuple pointer field. The chain lets the database pinpoint the required version. Version storage is therefore a key design consideration.

One approach is Append-Only — store all tuple versions in the same area. Since a lock-free doubly-linked list can't be maintained, the chain only goes one direction — old-to-new (O2N) or new-to-old (N2O).

Another approach is Time-Travel — store version info separately; the main table keeps primary-version data.

A third approach keeps primary versions in the main table, and keeps delta versions in a separate delta store. Updating an existing tuple requests a contiguous region from the delta store, writes a new delta version (holding only modified attributes), then in-place updates the primary version in the main table.

Each approach has tradeoffs and OLTP-workload implications. LSM trees fit the first approach naturally; chain-style version linking may not be explicit.

TAE currently picks a variant of the third approach:

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/Tae/mvcc.png?raw=true)

With heavy updates, LSM trees incur read amplification on older versions. TAE's version chain is buffer-manager-managed; when replaced, it merges with the main table into new blocks. Semantically in-place update; implementation-wise copy-on-write — which is required for cloud storage. New blocks have less read amplification — a benefit for AP queries over frequently-updated data.
