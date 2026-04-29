# Caching and Hot/Cold Data Separation

Data caching and hot/cold data separation is a key MatrixOne feature. It classifies data as hot or cold by access frequency and manages them with different storage strategies — achieving great performance while keeping operating costs low.

## Technical architecture

MatrixOne has two persistent storage components: the object store shared across the whole distributed cluster (the primary storage), and local storage on each compute node (CN) used mainly as a data cache. Primary storage holds the full cluster dataset; cache holds data fetched from primary storage during recent queries. CN memory is also used as part of the data cache.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/hot-cold-separation/cold-hot-data-separation.png width=60% heigth=60%/>
</div>

On query, the system first checks the connected CN's cache — memory first, then disk — for the requested data. On miss, it consults global metadata to check whether any other CN in that user's group has the data cached (memory then disk). If found, the request is routed to that CN, which handles it and returns results. If no CN has cached the data, the system reads from object storage and returns.

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/hot-cold-separation/query-order.png width=80% heigth=80%/>
</div>

When the user reads from object storage, the fetched blocks fill the cache in query order. E.g., 100MB fetched goes first to the connected CN's memory, then to its disk cache. Each new query updates the cache by the same rule. Both memory and disk evict via LRU — newest data is always the cheapest to fetch, colder data gradually leaves the cache.

## Product benefits

Caching + hot/cold separation brings several advantages. A simple example follows.

### Environment setup

The example assumes a distributed MatrixOne cluster — see [Deploy MatrixOne cluster](../../Deploy/deploy-MatrixOne-cluster.md).

1. Prepare a table `pe` and its CSV — the CSV is 35.8MB with 1,048,575 rows. Create two databases and load the same data into the `pe` table in each:

    ```sql
    create database stock;
    drop table if exists stock.pe;
    create table stock.pe (
    ts_code VARCHAR(255) DEFAULT null,
    trade_date VARCHAR(255) DEFAULT null,
    pe FLOAT DEFAULT null,
    pb FLOAT DEFAULT null
    );
    load data local infile '/XXX/pe.csv' into table stock.pe fields TERMINATED BY '\t';

    create database stock2;
    drop table if exists stock2.pe;
    create table stock2.pe (
    ts_code VARCHAR(255) DEFAULT null,
    trade_date VARCHAR(255) DEFAULT null,
    pe FLOAT DEFAULT null,
    pb FLOAT DEFAULT null
    );
    load data local infile '/XXX/pe.csv' into table stock.pe fields TERMINATED BY '\t';
    ```

2. Set up cache. In the cluster YAML, TN, Log Service, and CN all have cache-related settings. For queries, focus on the CN cache — primarily `memoryCacheSize` and `diskCacheSize`.

    ```yaml
    metadata:
      name: mo
      namespace: mo-hn
    spec:
      cnGroups:
      - name: cn-set1
        # intermediate config omitted
        sharedStorageCache: # core params for CN cache
          memoryCacheSize: 250Mi # CN memory cache, Mi = MB
          diskCacheSize: 1Gi # CN disk cache, Gi = GB
    ```

Setting both to `"1"` disables cache — all queries go directly to object storage, performance drops dramatically.

For a simpler demo, disable memory cache first and set only a limited disk cache. Since data compresses in storage, set disk cache to 20MB — about enough to hold the compressed 35.8MB file.

```yaml
metadata:
  name: mo
  namespace: mo-hn
spec:
  cnGroups:
  - name: cn-set1
## intermediate config omitted
    sharedStorageCache: # core params for CN cache
      memoryCacheSize: "1" # CN memory cache, Mi = MB
      diskCacheSize: 20Mi # CN disk cache, Gi = GB
```

### Query acceleration

After that, start the MatrixOne cluster and experience cache acceleration by running repeated queries — e.g., full-table scans on `stock.pe`:

```sql
mysql> select * from stock.pe into outfile "test01.txt";
Empty set (6.53 sec)

mysql> select * from stock.pe into outfile "test02.txt";
Empty set (4.01 sec)

mysql> select * from stock.pe into outfile "test03.txt";
Empty set (3.84 sec)

mysql> select * from stock.pe into outfile "test04.txt";
Empty set (3.96 sec)
```

The first query is slow (data fetched from object storage); subsequent queries are faster because the data is cached on disk.

### Cache eviction

Alternately scan `stock.pe` and `stock2.pe`:

```sql
mysql> select * from stock2.pe into outfile "test05.txt";
Empty set (5.84 sec)

mysql> select * from stock2.pe into outfile "test06.txt";
Empty set (4.27 sec)

mysql> select * from stock2.pe into outfile "test07.txt";
Empty set (4.15 sec)

mysql> select * from stock.pe into outfile "test08.txt";
Empty set (6.37 sec)

mysql> select * from stock.pe into outfile "test09.txt";
Empty set (4.14 sec)

mysql> select * from stock.pe into outfile "test10.txt";
Empty set (3.81 sec)
```

You'll see that switching tables slows queries down — because cache is small, fitting only one table's data. Each switch evicts old data; new queries re-fetch from object storage; repeat queries on the now-cached data are faster.

### Query warm-up

In many workloads, the volume or query complexity requires acceleration. MatrixOne's cache can warm data up to speed up queries.

E.g., this query:

```sql
SELECT pe1.ts_code, pe1.pe, pe1.pb
FROM stock2.pe as pe1
WHERE pe1.pe = (SELECT min(pe2.pe)
FROM stock2.pe as pe2
WHERE pe1.ts_code = pe2.ts_code)
ORDER BY trade_date
DESC LIMIT 1;
```

Without warm-up:

```sql
SELECT pe1.ts_code, pe1.pe, pe1.pb
FROM stock2.pe as pe1
WHERE pe1.pe = (SELECT min(pe2.pe)
FROM stock2.pe as pe2
WHERE pe1.ts_code = pe2.ts_code)
ORDER BY trade_date
DESC LIMIT

1;
+-----------+------+--------+
| ts_code   | pe   | pb     |
+-----------+------+--------+
| 000038.SZ |    0 | 1.2322 |
+-----------+------+--------+
1 row in set (5.21 sec)
```

This query only touches `stock2.pe`, so we can warm it by pre-scanning the full table:

```sql
mysql> select * from stock2.pe into outfile "test11.txt";
Empty set (6.48 sec)

mysql> SELECT pe1.ts_code, pe1.pe, pe1.pb FROM stock2.pe as pe1 WHERE pe1.pe = (SELECT min(pe2.pe) FROM stock2.pe as pe2 WHERE pe1.ts_code = pe2.ts_code) ORDER BY trade_date DESC LIMIT 1;
+-----------+------+---------+
| ts_code   | pe   | pb      |
+-----------+------+---------+
| 000068.SZ |    0 | 14.6959 |
+-----------+------+---------+
1 row in set (2.21 sec)
```

This works well for fixed reports — warm up data for the query, then execute to significantly improve query performance.
