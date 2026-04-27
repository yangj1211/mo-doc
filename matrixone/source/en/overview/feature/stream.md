# Streaming

## Characteristics of streaming data

With real-time analytics on the rise, streaming data has become increasingly important across many domains. Common sources include social-media live feeds, online retail transactions, real-time market analytics, network security monitoring, messaging, and smart-city infrastructure. Common applications:

- Real-time monitoring: network-traffic monitoring, online user behavior, IoT device state
- E-commerce platforms: real-time shopping behavior tracking, dynamic inventory, real-time pricing
- Real-time interactive apps: social-media real-time feeds, online-game player interactions
- Real-time risk management: anomaly detection in financial trading, security-threat detection
- Smart-city management: real-time traffic, public safety, environmental quality

Streaming data is defined by being real-time and continuous — it's produced constantly and transmitted immediately, always reflecting the latest state. Volumes are large and change fast — traditional processing approaches can't keep up, and more efficient techniques are required. Streaming typically requires:

- Real-time aggregation: summarizing and analyzing continuously arriving data in real time
- Dynamic data windows: analyzing streams over defined intervals for trend / pattern detection
- High throughput + low latency: handling large volumes while keeping processing immediate and accurate

These characteristics make streaming increasingly important for data-driven decisions — especially where fast response and real-time insight are needed.

## MatrixOne's streaming capabilities

### Source

MatrixOne syncs external streaming data with tables via `Source` — precise connection and mapping ensure seamless ingestion while preserving data integrity and accuracy.

### Dynamic Table

The Dynamic Table is the core of MatrixOne's streaming capability. Dynamic Tables capture, process, and transform inflows from `Source` and regular tables in real time — keeping information current and accurate across the system. This design lifts flexibility and efficiency, and improves responsiveness to complex data scenarios.
