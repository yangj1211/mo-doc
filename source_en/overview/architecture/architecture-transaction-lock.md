# Transactions and Locking

This article introduces implementation details of MatrixOne's transaction and lock mechanisms.

## MatrixOne transaction characteristics

MatrixOne supports pessimistic transactions and Read Committed (RC) isolation by default. Optimistic transactions with Snapshot Isolation (SI) are also supported — but optimistic and pessimistic transactions can't run simultaneously. In a cluster, you pick one model or the other.

## Transaction architecture

A MatrixOne cluster has three built-in services — CN (Compute Node), TN (Transaction Node), and LogService — plus an external object-storage service.

### CN (Compute Node)

CN handles most computation. Every transaction client (JDBC, MySQL client, etc.) connects to one CN and transactions are created there. Each transaction allocates a workspace on CN for temporary data. On commit, workspace data is sent to TN for commit processing.

### TN (Transaction Node)

TN processes commits from all CNs. It writes the commit log to LogService and writes committed data into memory. When in-memory data reaches a threshold, TN flushes it to external object storage and cleans up the corresponding logs.

### LogService

LogService is similar to a Write-Ahead Log system for TN. It uses Raft to replicate across multiple nodes for HA and strong consistency. MatrixOne can recover TN from LogService at any time.

LogService doesn't grow indefinitely — when logs hit a threshold, TN flushes corresponding data to object storage and truncates. The remaining in-memory logs are called LogTail — combined with object storage, they form the complete dataset.

### Clock

MatrixOne uses HLC (Hybrid Logical Clocks) integrated with the built-in MO-RPC for clock synchronization between CN and TN.

### Transaction reads

Reads happen at CN, which sees MVCC data versions depending on the transaction's `SnapshotTS`.

With `SnapshotTS` decided, the transaction needs two datasets — one in object storage, one in LogTail. Object storage is directly accessible from CN and cached for performance; LogTail lives in TN memory.

In old versions, CN ran in "Pull mode" — LogTail was synced from TN after transaction start — yielding poor performance, high latency, and low throughput. Starting with 0.8, MatrixOne uses "Push mode" — LogTail sync is no longer initiated at transaction start; CN-level subscriptions are used, and TN pushes delta LogTail to subscribing CNs every time LogTail changes.

In Push mode, each CN continuously receives LogTail pushes from TN, maintains the same in-memory structures as TN, and tracks the timestamp of the last consumed LogTail. When a transaction's `SnapshotTS` is decided, we just wait until the last-consumed LogTail timestamp ≥ `SnapshotTS` — then CN has the complete dataset for that `SnapshotTS`.

### Data visibility

A transaction's readable data depends on `SnapshotTS`.

If every transaction uses the current timestamp as `SnapshotTS`, it can read any data committed before. That always gives the newest data — at a performance cost.

In Pull mode, we must wait for TN to sync all transactions committed before `SnapshotTS`. The newer the snapshot, the more commits to wait for — higher latency.

In Push mode, CN must wait for all pre-`SnapshotTS` commits' LogTail to be consumed. Again, newer snapshots wait for more commits — higher latency.

But often you don't need the absolute newest data. MatrixOne provides two freshness levels:

1. Use the current timestamp as `SnapshotTS` — always newest.
2. Use CN's largest consumed LogTail timestamp as `SnapshotTS`.

Option 2 has almost zero transaction startup latency — it can immediately read/write because LogTail is ready — good performance and latency. But on the same DB connection, a later transaction may not see a prior transaction's writes if the LogTail for the prior commit hasn't reached the current CN yet — the later transaction would use an older `SnapshotTS` and miss those writes.

To address this, MatrixOne tracks two timestamps: CN-level last-transaction CommitTS (`CNCommitTS`) and session-level last-transaction CommitTS (`SessionCommitTS`). Two visibility levels (with `LastLogTailTS` = max LogTail timestamp consumed by current CN):

- **Session-level visibility**: `SnapshotTS = Max(SessionCommitTS, LastLogTailTS)` — preserves visibility within a session.

- **CN-level visibility**: `SnapshotTS = Max(CNCommitTS, LastLogTailTS)` — preserves visibility for transactions on the same CN.

## RC (Read Committed)

The prior sections covered MatrixOne transactions in general. MatrixOne previously supported only SI, implemented on MVCC with multiple data versions. MatrixOne now also supports RC.

Implementing RC on multi-version data: SI transactions maintain a consistent snapshot — the same data is visible throughout the transaction. RC reads the latest committed data — the consistent snapshot is no longer transaction-lifetime but per-query. Each query sets `SnapshotTS` to the current timestamp — ensuring the query sees previously committed data.

In RC, for write statements (UPDATE, DELETE, SELECT FOR UPDATE), if a write-write conflict appears, it means a concurrent transaction has modified the data. Since RC needs to see the latest writes, if the conflicting transaction has committed, we must update `SnapshotTS` and retry.

## Pessimistic transactions

This section covers MatrixOne's pessimistic-transaction design and implementation considerations.

### Key problems to solve

Implementing pessimistic transactions requires solving these:

#### Lock service

Lock service locks single records, ranges, or whole tables. When transactions need to lock resources during reads/writes, lock-wait must be supported on conflict. Deadlock-detection must exist to break deadlocks on cycles.

#### Scalable lock-service performance

MatrixOne transactions can happen on any CN. When many nodes access the lock service concurrently, it must scale.

#### Remove conflict detection at TN commit

In pessimistic mode, MatrixOne clusters have multiple TNs — we must ensure conflict detection at commit can be safely removed.

### Lock service

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/architecture/lockservice.png)

MatrixOne implements `LockService` for lock, unlock, conflict detection, lock waiting, and deadlock detection.

LockService isn't deployed as a separate component — it's a CN component. In a MatrixOne cluster, each CN's LockService instance knows the other instances and coordinates with them. Each CN only talks to its local LockService — it's oblivious to the others. From CN's perspective, the local LockService feels like a local component.

#### LockTable

Lock info is stored in LockTables — a LockService can contain many LockTables.

When a table's lock service is first accessed, LockService creates a LockTable instance attached to the current CN. Across the cluster, one LockTable has one local copy and multiple remote copies. Only the local LockTable actually stores lock info; remote copies are proxies to the local one.

#### LockTableAllocator

LockTableAllocator assigns LockTables — it tracks the LockTable distribution across the cluster in memory.

LockTableAllocator is a TN component. The binding between LockTable and LockService can change — e.g., if LockTableAllocator detects a CN going offline, the binding changes; each rebind increments a binding version number.

Between transaction start and commit, a LockTable-to-LockService binding may change. Inconsistency here can cause data conflicts — breaking pessimistic-transaction correctness. So LockTableAllocator runs at TN and, before processing commits, checks whether bindings have changed. If any accessed LockTable's binding is stale, the transaction is aborted to preserve correctness.

#### Distributed deadlock detection

Locks held by active transactions are distributed across LockTables in multiple LockServices — a distributed deadlock-detection mechanism is needed.

Each LockService has a deadlock-detection module with roughly:

- An in-memory wait queue per lock.

- On new conflict, the transaction is added to the holder's wait queue.

- Async task recursively checks all locks held by waiting transactions for cycles. For locks held by remote transactions, RPC gathers all locks held remotely.

#### Reliability

All critical lock-service data — lock info and LockTable-LockService bindings — lives in memory. On CN crash, connected transactions fail due to disconnection. LockTableAllocator then reassigns bindings — keeping lock service up.

LockTableAllocator runs in TN. When TN crashes, HAKeeper brings up a new TN, invalidating all bindings — every active transaction fails to commit due to binding mismatch.

### Using the lock service

To use locking effectively, MatrixOne provides a Lock operator that calls the lock service.

In the SQL planning phase, pessimistic transactions get special treatment — Lock operators are inserted at the right positions during execution.

- **INSERT**: plan inserts a Lock operator before Insert operators; subsequent operators run only after the lock is acquired.

- **DELETE**: similar — plan inserts a Lock operator before Delete operators; subsequent operators run only after the lock is acquired.

- **UPDATE**: plan splits update into Delete+Insert — so two locking phases (if PK isn't modified, this is optimized into one lock; the Insert phase won't lock).
