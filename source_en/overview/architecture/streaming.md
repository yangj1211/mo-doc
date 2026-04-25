# Stream Engine Architecture

MatrixOne has a built-in stream engine for real-time querying, processing, and enrichment of incoming data points (data streams). Developers can define and create stream-processing pipelines in SQL — serving them as a real-time data backend. They can also use SQL to query streaming data and join it with non-streaming data — further simplifying the overall data stack.

## Architecture

MatrixOne's stream-engine architecture:

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/overview/stream-arch.png width=80% heigth=80%/>
</div>

MatrixOne has a streaming-table creation mechanism, currently tightly integrated with Kafka. The goal is optimizing streaming data processing for large-scale time-series scenarios.

Under the hood, MatrixOne uses `Source` to efficiently connect and integrate with external streaming sources. Linking Dynamic Table with Source provides persistent storage and complex operations on incoming data — improving processing flexibility and efficiency.

### Source

Source bridges external data streams and MatrixOne database tables. Its precise connection + data-mapping mechanism ensures seamless ingestion with integrity and correctness.

Creating a new Source instance automatically generates a same-named Source table — a temporary data store that holds inflowing data and supports dynamic growth and real-time updates.

Currently MatrixOne only supports Kafka as a source, mapping via JSON. Syntax for creating a Source:

```sql
CREATE [OR REPLACE] SOURCE [IF NOT EXISTS] stream_name 
( { column_name data_type [KEY | HEADERS | HEADER(key)] } [, ...] )
WITH ( property_name = expression [, ...]);
```

For example, create a Source named `stream_test`:

```sql
create source stream_test(c1 char(25),c2 varchar(500),c3 text,c4 tinytext,c5 mediumtext,c6 longtext )with(
    "type"='kafka',
    "topic"= 'test',
    "partition" = '0',
    "value"= 'json',
    "bootstrap.servers"='127.0.0.1:9092'   
)
```

### Dynamic Table

Dynamic Table is MatrixOne's data pipeline concept. Dynamic Tables capture, process, and transform incoming data in real time — ensuring flows are immediately reflected and correctly expressed across the system. This design lifts flexibility and efficiency, and improves responsiveness to complex data scenarios.

Syntax for creating a Dynamic Table:

```sql
CREATE DYNAMIC TABLE [IF NOT EXISTS] table_name 
AS SELECT ... from stream_name ;
```

Example:

```sql
create dynamic table dt_test as select * from stream_test;
```
