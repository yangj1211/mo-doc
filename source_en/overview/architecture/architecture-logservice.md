# Log Service Architecture

Log Service plays an important role in MatrixOne — it's an independent service used by other components via RPC for log management.

Log Service uses the dragonboat library (a Go implementation of multi-Raft groups) for the Raft protocol — typically storing logs across multiple replicas on local disk, similar to WAL management. Transaction commits only need to write Log Service — no direct write to S3. Other components asynchronously batch data into S3. This gives low-latency commits with strong durability via multi-replica.

## Architecture

Log Service has a client and a server. The server includes the handler, dragonboat, and the Replicated State Machine (RSM). The client exposes key APIs. Their relationship:

<div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/logservice/logserviece-arch.png width=80% heigth=80%/>
</div>

### Client

The Log Service client is called primarily by TN and provides:

- `Close()`: close connection.
- `Config()`: get client config.
- `GetLogRecord()`: return a `pb.LogRecord` with an 8-byte LSN, 4-byte record type, and a `[]byte` data field (4-byte `pb.UserEntryUpdate`, 8-byte replica TN ID, plus payload).
- `Append()`: append `pb.LogRecord` to Log Service and return the LSN. The `pb.LogRecord` argument can be reused.
- `Read()`: read logs starting from `firstLsn` up to `maxSize`. The returned LSN becomes the next read start.
- `Truncate()`: delete logs up to a given LSN, freeing disk space.
- `GetTruncatedLsn()`: return the LSN of the most recent truncation.
- `GetTSOTimestamp()`: request N timestamps from the TSO (Timestamp Oracle). The caller owns `[returned_value, returned_value+count]`. Currently unused.

The client talks to the server over MO-RPC; the server interacts with `Raft` / `dragonboat` and returns results.

### Server

#### Server handler

The server receives requests and dispatches — entry point `(*Service).handle()`:

- **Append**: append log to Log Service — ultimately `(*NodeHost).SyncPropose()` for synchronous proposal. Wait until the log is committed and applied, then return the LSN of the written log.
- **Read**: read log entries from the log DB. First `(*NodeHost).SyncRead()` to linearly read up to the state machine's current LSN, then `(*NodeHost).QueryRaftLog()` to read entries from the log DB.
- **Truncate**: truncate logs in the log DB to free disk — actually just updates the most-recent truncate LSN in the state machine; no immediate physical truncate.
- **Connect**: establish a connection, and probe read/write on the state machine for health check.
- **Heartbeat**: includes Log Service, CN, and TN heartbeats. Updates state info in HAKeeper and syncs HAKeeper tick. On check, HAKeeper compares against tick — offline replicas trigger Remove / Shutdown.
- **Get XXX**: retrieve info from the state machine.

#### Bootstrap

Bootstrap runs at Log Service startup via the HAKeeper shard (shard ID 0). Entry point: `(*Service).BootstrapHAKeeper`.
Regardless of the configured replica count, each Log Service process starts one HAKeeper replica. At startup each replica sets `members`; the HAKeeper shard boots Raft with these as default replica count.
After Raft leader election, `set initial cluster info` runs — setting log-shard / TN-shard counts and log replica count.
After that, surplus HAKeeper replicas are stopped.

#### Heartbeat

These heartbeats flow from Log Service, CN, and TN to HAKeeper — not between Raft replicas. Two purposes:

1. Report replica state to HAKeeper so its state machine can update.
2. Return commands from HAKeeper that replicas should execute.

Log Service heartbeat flow is shown below — CN and TN flows are similar.

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/logservice/heartbeat.png)

By default heartbeats fire once per second:

1. At the storage level, generate heartbeat info for all shard replicas on this store — shard ID, node info, term, leader, etc.
2. Send the request to the Log Service server.
3. Server handles via `(*Service).handleLogHeartbeat()` and proposes to Raft.
4. HAKeeper's state machine handles via `(*stateMachine).handleLogHeartbeat()`:
    - Update state-machine LogState via `(*LogState).Update()` — refresh store and shard info.
    - Pick commands from `ScheduleCommands` and return them to the sender.

CN and TN heartbeats work similarly.

#### State machine (RSM)

Both Log Service and HAKeeper state machines are in-memory — data is memory-only. Both implement `IStateMachine`:

- `Update()`: after a proposal is committed (majority writes), `Update()` updates the state machine. Must be side-effect-free — identical input must produce identical output, or the state machine becomes unstable. Returns a Result; `error` is non-nil on failure.
- `Lookup()`: query state-machine data. An `interface{}` parameter specifies the data type; the return is `interface{}` too — users define their own data and type-assert. `Lookup()` is read-only.
- `SaveSnapshot()`: take a snapshot by writing state-machine data to `io.Writer` — typically a file handle — so the result usually lands on local disk. `ISnapshotFileCollection` represents external files (if any) to include in the snapshot. The third argument notifies the snapshot process if the Raft replica has stopped, to abort.
- `RecoverFromSnapshot()`: restore state-machine data from `io.Reader` (the most recent snapshot). `[]SnapshotFile` represents extra files to copy into the state-machine data dir. The third argument controls abort on Raft-replica stop.
- `Close()`: close and cleanup.

### Read / write flow

#### Write

1. If the connected node isn't the leader, forward to leader. Leader writes the log entry to local disk.
2. Leader sends the request asynchronously to followers — each writes the entry to disk.
3. When a majority completes, update the commit index and notify other followers via heartbeats.
4. Leader applies (`apply`) the entry to its state machine.
5. On apply completion, return to the client.
6. Followers apply in their own state machines after receiving the commit index.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/logservice/write.png width=80% heigth=80%/>
</div>

#### Read

Two read paths:

- Read from the state machine.

    - Client issues a read; when it arrives at the leader, the current commit index is recorded.
    - Leader sends heartbeats to all nodes to confirm its leadership — once a majority responds, leadership is re-confirmed and we can reply.
    - Wait until apply index ≥ commit index.
    - Read from the state machine and return.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/logservice/read.png width=80% heigth=80%/>
</div>

- Read log entries from the log DB.

    - Typically during cluster restart.
    - On restart, a replica first restores state-machine data from a snapshot, then reads log-DB entries starting from the snapshot's index and applies them to the state machine.
    - Only then can the replica participate in leader election.
    - After the cluster elects a leader, TN connects to the Log Service cluster and reads log entries from one replica's log DB starting at the previous checkpoint position — replaying them into its own in-memory data.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/logservice/logdb-read.png width=50% heigth=50%/>
</div>

### Truncation

As Log Service log entries accumulate in the log DB, disk fills up. Disk must be freed periodically — via truncation.

Log Service uses an in-memory state machine — it stores only metadata and state (tick, state, LSN, etc.), no user data. User data is kept by TN. Think of it as a master/slave architecture where state machines are separated — TN and Log Service each maintain their own.

Under this separation, naive snapshotting causes problems:

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/logservice/truncation-1.png width=60% heigth=60%/>
</div>

1. TN sends a truncate request with truncate index 100, but Log Service state machine applied index is 200 — logs before 200 would be deleted and a snapshot taken at 200. Note: truncate index ≠ applied index.
2. The cluster restarts.
3. Log Service applies the snapshot at index 200, sets the first index to 200 (logs before 200 are gone), then replays remaining logs and serves.
4. TN reads log entries from Log Service starting at 100 — but entries before 200 are missing, so the read fails.

To fix this, truncation now works as follows:

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/logservice/truncation-2.png width=70% heigth=70%/>
</div>

1. TN sends a truncate request that updates the truncate LSN in the Log Service state machine — no snapshot/truncate is done yet.
2. A truncation worker inside each Log Service server sends truncate requests periodically. The `Exported` parameter is set to `true` — the snapshot isn't visible to the system, it's just exported to a designated directory.
3. The truncation worker checks exported snapshots for ones with index greater than the truncate LSN. The one closest to the truncate LSN is imported into the system and made visible.
4. All replicas perform the same action so snapshot LSNs stay consistent across state machines — guaranteeing the expected entries are readable after restart.
