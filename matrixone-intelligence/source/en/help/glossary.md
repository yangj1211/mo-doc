# **Glossary**

### **Terms**

These short definitions can help you build the right mental model when reading the rest of the docs.

|  Term   | Definition   |
|  ----  | ----  |
| A  |  |
| AST  | Abstract Syntax Tree — the tree representation of code, a fundamental piece of a compiler. |
| C  |  |
| Cluster  | The distributed deployment form of MatrixOne, made up of multiple hosts that act as a single logical system. |
| E  |  |
  | Explicit Transaction | A transaction in which you explicitly decide which set of operations must succeed or fail together, controlled with `BEGIN TRANSACTION` and `ROLLBACK TRANSACTION` / `COMMIT TRANSACTION`. |
  | I |  |
  | Implicit Transaction | An auto-commit transaction. |
  | O |  |
  | Optimistic Transaction | A transaction that does no conflict detection or locking when it starts; it caches the relevant data in memory and applies inserts / updates / deletes against it. |
  | P |  |
  | Pessimistic Transaction | The default transaction model in MatrixOne. When the transaction starts, it assumes write contention is possible and locks the relevant tables or rows in advance; insert / update / delete are buffered in memory and persisted only on commit (or discarded on rollback), with the locks released. |
  | S  |  |
  | Snapshot Isolation (SI) | A widely used multi-version concurrency control technique. MatrixOne supports distributed transactions at Snapshot Isolation. |

### **Key concepts**

|  Concept   | Definition   |
|  ----  | ----  |
| A  |  |
| Auto-Rebalance  | In a distributed system, the automatic process of rebalancing storage and read/write load across multiple servers. |
| C  |  |
| Consistency  | MatrixOne provides strong consistency, guaranteeing that once a write succeeds, the latest data is visible from every Store (node). |
| E  |  |
| Execution Plan  | A graph representation of query operations produced by the query optimizer, describing the most efficient way to execute the query. |
| F  |  |
| Fault-Tolerance  | The ability of the system to keep running after one or more components fail. |
| M  |  |
| Monolithic Engine  | A hyper-converged engine that supports mixed workloads — TP, AP, time-series, machine learning. |
| Materialized View  | A pre-computed dataset, persisted for later reuse, typically used to speed up queries. |
| Metadata  | Data describing the structural information of data in a database. |
| P  |  |
| Paxos  | A consensus algorithm that keeps a group of distributed computers communicating asynchronously in agreement. |
| R  |  |
| Raft  | A consensus algorithm easier to understand than Paxos, comparable in fault tolerance and performance. |
| Raft Group and Leader | Raft defines a leader and several followers in a group. The group represents a replicated state machine; only the leader handles client requests, then propagates them to followers. |
| S  |  |
| SIMD instruction | Single Instruction / Multiple Data — a way to process multiple pieces of data with one instruction. |
| T  |  |
| Transaction |  A series of operations against the database that satisfies the basic ACID requirements. |
| TAE | Transactional Analytic Engine — the storage engine. The storage engine is the main interface of the storage layer; TAE supports both row and columnar storage and transactional processing. |
| V  |  |
| Vectorized Execution  | By making efficient use of CPU caches, vectorized execution speeds up analytical query engines. Arrow's columnar format enables lightweight techniques such as dictionary encoding, bit packing, and run-length encoding, all of which further improve query efficiency. |
