# 使用 modump 导出数据

MatrixOne Intelligence 支持使用 `mo-dump` 导出数据。

## 什么是 `mo-dump`

`mo-dump` 是 MatrixOne 的一个客户端实用工具，与 `mysqldump` 一样，它可以被用于通过导出 `.sql` 类型的文件来对 MatrixOne 数据库进行备份，该文件类型包含可执行以重新创建原始数据库的 SQL 语句。

使用 `mo-dump` 工具，你必须能够访问运行 MatrixOne 实例的服务器。你还必须拥有导出的数据库的用户权限。

### `mo-dump` 语法结构

```
./mo-dump -u ${user} -p${password} -h ${host} -P ${port} -db ${database} [--local-infile=true] [-csv] [-tbl ${table}...] -net-buffer-length ${net-buffer-length} > {dumpfilename.sql}
```

**参数释义**

- **-u [user]**：连接 MatrixOne 服务的用户名。只有具有数据库和表读取权限的用户才能使用 `mo-dump` 实用程序，默认值：dump。

- **-p [password]**：MatrixOne 用户的有效密码。

- **-h [host]**：MatrixOne 服务的主机 IP/HOST 地址。默认值：127.0.0.1。

- **-P [port]**：MatrixOne 服务的端口。默认值：6001。

- **-db [数据库名称]**：必需参数。要备份的数据库的名称。可以指定多个数据库，数据库名称之间用 `,` 分隔。

- **-net-buffer-length [数据包大小]**: 数据包大小，即 SQL 语句字符的总大小。数据包是 SQL 导出数据的基本单位，如果不设置参数，则默认 1048576 Byte（1M），最大可设置 16777216 Byte（16M）。假如这里的参数设置为 16777216 Byte（16M），那么，当要导出大于 16M 的数据时，会把数据拆分成多个 16M 的数据包，除最后一个数据包之外，其它数据包大小都为 16M。

- **-no-data**: 默认值为 false。当设置为 true 时表示不导出数据，仅导出表结构。

- **-csv**：默认值为 false。当设置为 true 时表示导出的数据为 csv 格式，生成数据库和表结构以及导入的 SQL 语句将会保存在生成的 sql 文件中，而数据则导出到当前目录下生成的 ${databaseName} _${tableName}. csv 文件中。

- **--local-infile**：默认值为 true，仅在参数 -csv 设置为 true 时生效。当参数为 true 时，mo-dump 输出的 sql 文件脚本中为 LOAD DATA LOCAL INFILE。当参数为 false 时，mo-dump 输出的 sql 文件脚本中为 LOAD DATA INFILE。

- **-tbl [tableName]**：可选参数。如果参数为空，则导出整个数据库。如果要备份指定表，则可以在命令中添加参数 `-tbl` 和 `tableName`。如果指定多个表，表名之间用 `,` 分隔。

- **> {importStatement.sql}**：将输出的 SQL 语句存储到文件 *importStatement.sql* 中，否则在屏幕上输出。

## 如何使用 `mo-dump`

### 安装 mo-dump 工具

下载方式一和下载方式二需要先安装下载工具 wget 或 curl，如果你未安装，请先自行安装下载工具。

- macOS 下安装

:::::{tab-set}

::::{tab-item} **下载方式一：`wget` 工具下载二进制包**
 x86 架构系统安装包：

 ```
 wget https://github.com/matrixorigin/mo_dump/releases/download/1.0.0/mo-dump-1.0.0-darwin-x86_64.zip
 unzip mo-dump-1.0.0-darwin-x86_64.zip
 ```

 ARM 架构系统安装包：

 ```
 wget https://github.com/matrixorigin/mo_dump/releases/download/1.0.0/mo-dump-1.0.0-darwin-arm64.zip
 unzip mo-dump-1.0.0-darwin-arm64.zip
 ```

如 github 原地址下载过慢，您可尝试从以下地址下载镜像包：

```
wget  https://githubfast.com/matrixorigin/mo_dump/releases/download/1.0.0/mo-dump-1.0.0-darwin-xxx.zip
```
::::

::::{tab-item} **下载方式二：`curl` 工具下载二进制包**
 x86 架构系统安装包：

 ```
 curl -OL https://github.com/matrixorigin/mo_dump/releases/download/1.0.0/mo-dump-1.0.0-darwin-x86_64.zip
 unzip mo-dump-1.0.0-darwin-x86_64.zip
 ```

 ARM 架构系统安装包：

 ```
 curl -OL https://github.com/matrixorigin/mo_dump/releases/download/1.0.0/mo-dump-1.0.0-darwin-arm64.zip
 unzip mo-dump-1.0.0-darwin-arm64.zip
 ```

如 github 原地址下载过慢，您可尝试从以下地址下载镜像包：

```
curl -OL https://githubfast.com/matrixorigin/mo_dump/releases/download/1.0.0/mo-dump-1.0.0-darwin-xxx.zip
```
::::
:::::
- Linux 下安装

:::::{tab-set}

::::{tab-item} **下载方式一：`wget` 工具下载二进制包**
 x86 架构系统安装包：

 ```
 wget https://github.com/matrixorigin/mo_dump/releases/download/1.0.0/mo-dump-1.0.0-linux-x86_64.zip
 unzip mo-dump-1.0.0-linux-x86_64.zip
 ```

 ARM 架构系统安装包：

 ```
 wget https://github.com/matrixorigin/mo_dump/releases/download/1.0.0/mo-dump-1.0.0-linux-arm64.zip
 unzip mo-dump-1.0.0-linux-arm64.zip
 ```

如 github 原地址下载过慢，您可尝试从以下地址下载镜像包：

```
wget  https://githubfast.com/matrixorigin/mo_dump/releases/download/1.0.0/mo-dump-1.0.0-linux-xxx.zip
```
::::

::::{tab-item} **下载方式二：`curl` 工具下载二进制包**
 x86 架构系统安装包：

 ```
 curl -OL https://github.com/matrixorigin/mo_dump/releases/download/1.0.0/mo-dump-1.0.0-linux-x86_64.zip
 unzip mo-dump-1.0.0-linux-x86_64.zip
 ```

 ARM 架构系统安装包：

 ```
 curl -OL https://github.com/matrixorigin/mo_dump/releases/download/1.0.0/mo-dump-1.0.0-linux-arm64.zip
 unzip mo-dump-1.0.0-linux-arm64.zip
 ```

如 github 原地址下载过慢，您可尝试从以下地址下载镜像包：

```
curl -OL https://githubfast.com/matrixorigin/mo_dump/releases/download/1.0.0/mo-dump-1.0.0-linux-xxx.zip
```
::::
:::::
:::{note}
由于 linux 内核的限制，mo-dump 在低版本内核（低于 5.0）的 OS 上可能会出现无法正常运行的情况，此时需要升级您的内核版本。
:::
### 使用 `mo-dump` 导出 MatrixOne Intelligence 的数据库

`mo-dump` 在命令行中非常易用。参见以下步骤示例，导出 *sql* 文件格式完整数据库：

1. 选择目标实例，点击**连接 > 通过第三方工具连接**，右侧滑窗内可查阅到 MatrixOne Intelligence 上你的实例主机地址、端口号、用户名和密码。

    :::{note}
    mo-dump 暂不支持连接串的用户名格式（即不支持原格式 `<accountname>:<username>:<rolename>`)，需要更改为 `<accountname>#<username>#<rolename>`。
    :::
2. 在你本地计算机上打开终端窗口，输入以下命令，连接到 MatrixOne Intelligence，并且导出数据库：

    ```
    ./mo-dump -u <accountname>#<username>#<rolename> -p password -h moc_host_address -P 6001 -db database > exported_db.sql
    ```

## 示例

**示例 1**

如果你想要生成单个或多个数据库以及其中所有表的备份，请运行以下命令。该命令将在 *importMydb.sql* 文件中生成 **mydb1** 和 **mydb2** 数据库以及表的结构和数据的备份。*importMydb.sql* 文件会保存在当前目录下：

```
./mo-dump -u <accountname>#<username>#<rolename> -p password -h moc_host_address -P 6001 -db mydb1,mydb2 > importMydb.sql
```

**示例 2**

如果你想将数据库 *mydb* 内的表的数据导出为 *CSV* 格式，数据库 *mydb* 中的所有表的数据将会以 `${databaseName}_${tableName}.csv` 的格式导出在当前目录下，生成数据库和表结构以及导入的 SQL 语句将会保存在 *importMydbWithCsv.sql* 文件中：

```
./mo-dump -u <accountname>#<username>#<rolename> -p password -h moc_host_address -P 6001 -db mydb -csv > importMydbWithCsv.sql
```

**示例 3**

如果要在数据库中指定生成某一个表或者某几个表的备份，可以运行以下命令。该命令将生成数据库 *db1* 中 *t1* 表和 *t2* 表的结构和数据备份，保存在 *tab2.sql* 文件中。

```
./mo-dump -u <accountname>#<username>#<rolename> -p password -h moc_host_address -db db1 -tbl t1,t2 > tab2.sql 
```

**示例 4**

如果要在数据库中某一个表或者某几个表的结构备份，可以运行以下命令。该命令将生成数据库 *db1* 中 *t1* 表和 *t2* 表的结构，保存在 *tab_nodata.sql* 文件中。

```
./mo-dump -u <accountname>#<username>#<rolename> -p password -h moc_host_address -db db1  -no-data -tbl t1,t2 > tab_nodata.sql
```

## 限制

- `mo-dump` 暂不支持只导出数据。如果你想在没有数据库和表结构的情况下生成数据的备份，那么，你需要手动拆分 `.sql` 文件。

- `mo-dump` 仅支持导出属于用户自己的数据库，所以在发布订阅中，订阅端通过 `mo-dump` 导出订阅库的 sql 只有订阅语句。
