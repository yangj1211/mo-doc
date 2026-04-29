# MatrixOne Feature Overview

## MatrixOne capabilities

In MatrixOne v25.2.2.2, the following capabilities help you work efficiently:

### Distributed architecture

MatrixOne uses a distributed compute-storage separation architecture. Separating storage, data, and compute lets MatrixOne flexibly scale when resources bottleneck. Multi-node architectures also allow more efficient resource allocation and reduce hotspots and contention.

### Transactions and isolation

MatrixOne uses optimistic transactions with Snapshot Isolation.

In a distributed architecture, optimistic transactions achieve better performance through fewer conflicts. Their implementation also supports the stronger Snapshot Isolation level. To uphold ACID, MatrixOne currently supports Snapshot Isolation exclusively — it's stricter than the common Read Committed, effectively preventing dirty reads, and is a better fit for distributed optimistic transactions.

### Cloud-native

MatrixOne is a cloud-native database. Storage supports local disk, AWS S3, NFS, etc. — File Service provides a uniform abstraction across backends. MatrixOne clusters run stably across infrastructure environments, adapting to enterprise private clouds and major public clouds.

### Load balancing

In distributed databases, load naturally varies across nodes — potentially bottlenecking some workloads or wasting compute. MatrixOne implements compute-resource load balancing to keep resource allocation balanced across nodes.

### SQL routing

SQL routing was commonly used in early shard-per-database/table scenarios to decide which instance / database / table a SQL request should run against.

In MatrixOne, even though the storage engine no longer limits database scale, load balancing across CNs and resource isolation between tenants remain relevant. SQL routing sends requests to specific CNs per rules, addressing cases where a single database instance can't handle a large access load.

### IP allow-lists

An allow-list is a security policy controlling access to restricted resources, systems, or networks. The idea is simple: only authorized / trusted entities are permitted; others are rejected. Authorized entities may include specific users, IP addresses, applications, or others. The opposite — a deny-list — blocks specifically listed entities while allowing everything else.

Characteristics of allow-lists:

- Only users / systems defined up-front can access; everything else is blocked.
- Allow-lists raise security but may constrain legitimate users — balance security and convenience.
- In databases, allow-lists primarily restrict user access — only specific users or specific servers / subnets can access the database, raising security.

### Multi-tenancy

A single-cluster, multi-tenant model offers resource sharing, simpler administration, better scalability, and security isolation — ideal when one platform needs to serve many tenants.

MatrixOne's multi-tenant mode provides independent database instances per tenant with logical isolation, effectively preventing leaks and tampering.

## MatrixOne performance advantages

### Efficient storage

MatrixOne selects AWS S3 as an efficient storage backend, addressing low cost and hot/cold tiering:

- Low cost: reduced redundancy yields acceptable performance at lower cost.
- Hot/cold separation: an enabler for fine-grained data management.

### Clear transaction roles

- CN handles compute and transaction logic; TN keeps metadata, logs, and arbitrates transactions.
- A Logtail object in logs preserves data for recent logs. Logtail is periodically persisted to S3. New CNs can pull Logtail into their cache in real time — effectively sharing partial data.
- A transaction size threshold is applied: transactions above it go directly to S3, with only the write recorded in the log; smaller transactions go through TN, dramatically increasing throughput.

### HTAP workload isolation

As an HTAP database, MatrixOne isolates workload types:

- Server-level isolation: with sufficient hardware, each component runs on its own physical machine, sharing object storage.
- Container-level isolation: when hardware is limited, stateless nodes allow container-level isolation as the partitioning means.

### Flexible resource allocation

Business mixes change over time — resource mixes need flexibility. Old architectures couldn't adjust on the fly; MatrixOne implements fine-grained node management, including:

- CN role allocation: CNs can be partitioned for TP or AP. Scale out the relevant CN group when a workload bottlenecks.
- Dynamic load detection across CN groups — idle resources automatically shift to busy groups.
- Logical resource isolation per tenant (`ACCOUNT`) — tenants can use dedicated or shared CNs.
