---
orphan: true
---

# Data Branch

A **data branch** is MatrixOne's lightweight data version-management capability. If you are familiar with Git, think of it as **Git branches at the database layer**: create an independent, fully writable data copy from a point in time, modify it freely, and never touch the original.

## How it works

Data branches are built on MatrixOne's **MVCC + zero-copy snapshots**. When you create a branch, the system only records a logical reference pointing to the current data version — no physical copying happens. Subsequent writes on the branch go through copy-on-write and only record incremental pages; the original pages stay untouched.

As a result, branch creation is an **O(1) operation** — whether the source table has 100 rows or 100 billion rows, creating a branch completes in milliseconds with nearly zero added storage.

A branch's lifecycle is fully independent. When deleted, only pages unique to that branch are reclaimed. When merged back into the trunk, incremental changes are applied as an atomic transaction.

:::{note}
This feature requires **MatrixOne v3.0 or later**. In v2.x the closest feature is called "Database Clone", with slightly different syntax and no merge support.
:::

## Typical use cases

- **Development & debugging** — branch off production data, validate new SQL on real distributions, no desensitized exports needed
- **A/B testing** — create two branches on the same data and run different pipelines in parallel to compare results
- **Rollback insurance** — create a branch before a risky operation as a safety net; one command to revert if things go wrong
- **Data sharing** — hand downstream teams a read-only branch so their analytics don't hit the main database, and they never see the latest production writes
- **Release validation** — branch before a major release, run canary checks, then merge

## Branch vs. Snapshot

Both rely on MVCC internals, but they serve different scenarios:

| Dimension | Data Branch | Snapshot |
|-----------|------------|----------|
| Writable | Yes, read/write | No, read-only |
| Lifecycle | Long-lived, mergeable | Typically transient |
| Typical use | Parallel dev / A/B / canary | Backup / audit / time-travel query |
| Creation cost | O(1) | O(1) |
| Storage | Delta + unique pages | Metadata only |
| Merge support | Yes | No |

Rule of thumb: **use a branch when you need to write; use a snapshot when you only need to read**.

:::{seealso}
Related SQL syntax: [CREATE SNAPSHOT](../sql-reference/snapshot.md)
:::
