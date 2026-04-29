# 5-Minute Quickstart

This guide walks you through running MatrixOne end-to-end in 5 minutes — creating a database, a table, inserting data, and verifying with a query. Suitable for developers who already have Docker installed.

## Prerequisites

- Docker 20.10 or later
- A MySQL client (or any MySQL-compatible tool like DBeaver or Navicat)
- Port `6001` available

:::{tip}
If you just want to quickly explore MatrixOne's SQL capabilities, try the <a href="#">online sandbox</a> (placeholder link) directly in your browser.
:::

## Steps

1. **Pull the image**

   ```bash
   docker pull matrixorigin/matrixone:latest
   ```

2. **Start the container**

   ```bash
   docker run -d --name mo \
     -p 6001:6001 \
     matrixorigin/matrixone:latest
   ```

   Startup takes about 10-30 seconds while the instance initializes its metadata.

3. **Connect to the database**

   ```bash
   mysql -h 127.0.0.1 -P 6001 -u dump -p111
   ```

4. **Create a table and insert data**

   ```sql
   CREATE DATABASE demo;
   USE demo;

   CREATE TABLE users (
     id          INT PRIMARY KEY,
     name        VARCHAR(64),
     created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );

   INSERT INTO users (id, name) VALUES
     (1, 'Alice'),
     (2, 'Bob'),
     (3, 'Charlie');
   ```

5. **Verify with a query**

   ```sql
   SELECT COUNT(*) AS total FROM users;
   ```

   Expected result:

   ```text
   +-------+
   | total |
   +-------+
   |     3 |
   +-------+
   1 row in set
   ```

:::{warning}
The default password `111` shipped with the container is intended for local experimentation only. **Change it before deploying to production** — see <a href="#">Security Configuration</a>.
:::

## Next

:::{card} 📐 &nbsp;Explore core concepts
:link: ../concepts/data-branch
:link-type: doc
:class-card: mo-entry-card

Before diving into SQL, meet MatrixOne's core design ideas: data branches, snapshots, and the unified HTAP engine.
:::
