# Logtail Protocol

Logtail is the log-sync protocol between CN (Compute Node) and TN (Transaction Node) — the cornerstone of CN-TN coordination. This article covers positioning, protocol content, and generation.

TAE is MatrixOne's cloud-native transactional + analytical engine. TN's responsibilities include:

- Processing committed transactions.
- Serving Logtail to CN.
- Dumping the latest transactional data to object storage and advancing the log window.

(1) and (3) produce state changes — e.g., data successfully written to memory or object storage. Logtail is a log-sync protocol designed to cheaply sync a subset of TN state so that CN can rebuild locally readable data. Logtail has these characteristics:

- Chains CN and TN together — essentially a log-replicated state machine letting CN sync TN's partial state.
- Two fetch modes: pull and push.

    - Push is more real-time — continuously syncs delta logs from TN to CN.
    - Pull supports snapshot sync over a given time range, and fetch of delta logs on demand.

- Logtail supports table-level subscription and collection — more flexible for multi-CN support, helping balance CN load.

## Protocol content

Logtail has two parts: in-memory data and metadata — the difference being whether data has been flushed to object storage.

Before flush, a committed transaction's updates exist in Logtail as in-memory data. Any modification ultimately reduces to insert or delete:

- For insert, Logtail info includes row-id, commit-timestamp, and the columns from the table definition.
- For delete, Logtail info includes row-id, commit-timestamp, and PK columns. Upon receiving in-memory data, CN organizes it into a B-tree structure in memory to serve queries.

Keeping memory data forever would bloat CN memory. Based on time or capacity, in-memory data is flushed to object storage, forming an object. Each object contains one or more blocks. A block is the smallest storage unit — currently capped at 8192 rows. After flush, Logtail passes block metadata to CN; CN filters visible blocks by transaction timestamp, reads block contents, combines with in-memory data, and gets a complete data view for a point in time.

Plus, performance optimizations bring extra detail:

### 1. Checkpoint

When TN runs for a while, it performs a checkpoint — dumping all prior data to object storage. All that metadata is rolled into a "package". When a new CN connects and requests its first Logtail, if its subscription timestamp is greater than the checkpoint timestamp, TN can pass the checkpoint metadata (a string) via Logtail — so CN can directly read block information generated before the checkpoint. This lightens the network load of sending block metadata from scratch and reduces TN IO pressure.

### 2. Memory cleanup

When TN passes block metadata to CN, it cleans up previously-passed in-memory data by block ID. During TN flush, data updates may happen — e.g., the block being flushed might receive new deletes. If the policy were rollback + retry, already-written data would be invalidated. In update-heavy workloads, this generates many rollbacks, wasting TN resources. To avoid it, TN continues committing — in-memory data produced after a flush began can't be removed from CN. The block meta carries a timestamp inside which CN can clean its in-memory data for the block. Unmerged updates are asynchronously flushed in the next flush and removed via CN.

### 3. Faster reads

Blocks already flushed may continue producing deletes — reads on those blocks must combine with in-memory deletes. CN keeps an extra B-tree index of blocks so it can quickly know which ones to combine with in-memory data. Logtail application must carefully update this index — add entries when processing in-memory data, remove them when processing block metadata. Only blocks in this index need in-memory-data checks — with many blocks, this is a large performance win.

## Generating Logtail

Logtail has pull and push modes — distinct characteristics of each are below.

### 1. Pull

Pull syncs table snapshots plus subsequent delta logs.

To achieve this, TN maintains a `logtail table` — a list of `txn handle` sorted by transaction prepare time. Given any time, binary search finds in-range `txn handle`, then each handle exposes which blocks the transaction updated; traversing these blocks gives a complete log. To accelerate lookup, handles are paged — a page's `bornTs` is the min prepare time among its handles. The first binary-search level targets pages.

Based on `logtail table`, receiving a pull request works like:

1. Adjust the request's time range based on existing checkpoints — earlier parts come from checkpoints.
2. Take a snapshot of the logtail table. Use `RespBuilder` (visitor pattern) to iterate relevant txn handles and gather committed log info.
3. Transform the collected log info per the Logtail protocol and return to CN.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/architecture/logtail-arch-1.png width=70% heigth=70%/>
</div>

```
type RespBuilder interface {
  OnDatabase(database *DBEntry) error
  OnPostDatabase(database *DBEntry) error
  OnTable(table *TableEntry) error
  OnPostTable(table *TableEntry) error
  OnPostSegment(segment *SegmentEntry) error
  OnSegment(segment *SegmentEntry) error
  OnBlock(block *BlockEntry) error
  BuildResp() (api.SyncLogtailResp, error)
  Close()
}
```

### 2. Push

Push syncs delta logs from TN to CN in a more real-time way. Phases: subscribe, collect, push.

- **Subscribe**: after a new CN starts, as client it opens an RPC stream to the TN server and subscribes to catalog-related tables. Once basic info (database, table, column) is synced, CN can serve traffic. When TN receives a subscribe request for a table, it does a pull first — including all Logtail up to the last push timestamp in the subscription response. Currently for a CN, Logtail subscribe / unsubscribe / data push all happen on one RPC stream; any error triggers a reconnect in CN until recovery. After subscription succeeds, subsequent Logtail is delta-push only.

- **Collect**: at TN, after a transaction's WAL write completes, a callback runs and collects Logtail inside the transaction. The main flow traverses the `workspace` TxnEntry (the basic transaction-update container directly involved in the commit pipeline); based on its type, it converts log info into Logtail-format data. Collection runs through a pipeline concurrent with WAL fsync — reducing blocking.

- **Push**: Push filters — if a CN hasn't subscribed to a table, skip it.

What if a table isn't updated for a long time — how does CN know? A heartbeat mechanism — default 2ms. TN's commit queue receives a heartbeat empty transaction that does no real work but consumes a timestamp, triggering a heartbeat Logtail push — informing CN that all earlier tables have been synced and pushing forward CN's timestamp watermark.

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/architecture/logtail-arch-2.png)
