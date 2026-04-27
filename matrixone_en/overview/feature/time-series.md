# Time-series Capabilities

## Characteristics of time-series data

With IoT, time-series databases are increasingly needed — smart-car telemetry, factory-equipment monitoring, financial trading tick data, and more. Common scenarios include:

- Monitoring software systems: virtual machines, containers, services, applications
- Monitoring physical systems: water-resource monitoring, manufacturing equipment, national-security-related monitoring, telecoms, sensors, glucose meters, blood pressure, heart rate, etc.
- Asset-tracking applications: cars, trucks, physical containers, freight pallets
- Financial trading systems: traditional securities and emerging crypto currencies
- Event applications: tracking user / customer interactions
- BI tools: tracking KPIs and overall business health
- Internet: user web-browsing behavior, application log data

Time-series data keeps growing over time; volumes are massive — tens of millions or billions of records per second. Common patterns include:

1. Fetch latest state — the most recent data (e.g., latest sensor values).
2. Interval statistics — average / max / min / count over a time range.
3. Anomaly filtering — filter by conditions.

## MatrixOne time-series capabilities

Dedicated NoSQL time-series databases exist (InfluxDB, OpenTSDB, TDEngine…); MatrixOne is different — it's a general-purpose database still focused on HTAP CRUD and data analytics, still uses relational modeling, and still uses classic SQL. MatrixOne adds time-series capabilities on top — closer in spirit to TimeScaleDB. Functionally it supports time windows, downsampling, interpolation, and partitions; performance targets high throughput, high compression, and real-time analytics. Architecturally, strong scalability, hot/cold separation, and read/write separation fit time-series well — plus MatrixOne retains updates and transactions. So MatrixOne fits hybrid scenarios where you develop with a general-purpose relational database but need time-series capabilities.

MatrixOne's time-series capabilities include:

- Common types (string, numeric, date/time) plus new workloads (JSON, vector). See [Data Types](../../Reference/Data-Types/data-types.md).
- Dedicated time-series tables with timestamp PK and arbitrary dimension / metric columns. See [Time windows](../../Develop/read-data/window-function/time-window.md).
- Common time-window capabilities — downsample by different intervals. See [Time windows](../../Develop/read-data/window-function/time-window.md).
- Interpolation strategies for nulls. See [Time windows](../../Develop/read-data/window-function/time-window.md).
- Simple and complex queries common to traditional databases. See [Single-table queries](../../Develop/read-data/query-data-single-table.md), [Joins](../../Develop/read-data/multitable-join-query.md), [Subqueries](../../Develop/read-data/subquery.md), [Views](../../Develop/read-data/subquery.md), [CTEs](../../Develop/read-data/cte.md).
- Fast [bulk import](../../Develop/import-data/bulk-load/bulk-load-overview.md), [streaming writes](../../Develop/import-data/stream-load.md), and [`INSERT INTO`](../../Develop/import-data/insert-data.md).
- A full set of [aggregate functions](../../Reference/Functions-and-Operators/Aggregate-Functions/count.md) to meet time-series computation.
