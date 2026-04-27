# 连接器

MatrixOne Intellogence 平台提供了一个强大的数据连接器，用于支持数据的载入和导出，允许用户轻松地将存储在对象存储和分布式文件系统上的数据导入到 MatrixOne Intellogence 平台中。只需提供必要的连接信息，即可实现数据的无缝导入，为后续的数据分析和处理提供便利。

## 支持连接器

   | 类型          | 连接器        |载入   |导出         |
   |---------------|-------------|-------|-----------|
   | 对象存储       | 阿里云 OSS   | ✅      | ✅   |
   | 对象存储       | 标准 S3       | ✅      | ✅   |
   | 分布式文件系统  | HDFS        | ✅      | ❌  |
   | 数据库         | MatrixOne   | ❌      | ✅   |
   | 知识库         | Dify        | ❌      | ✅   |

## 如何使用连接器

进入到 MatrixOne Intelligence 工作区，依次点击**数据接入**>**连接器**>**创建连接器**，选择需要连接的数据源类型。

### 对象存储

#### 阿里云 OSS

要将文件从阿里云 OSS 导入至 MatrixOne Intelligence 平台，或将处理结果导出至 OSS，您需提供以下连接配置信息：

- 地区：OSS 服务的访问地址。
- AccessKeyId: 您的阿里云账号的 AccessKey ID。
- AccessKeySecret: 您的阿里云账号的 AccessKey Secret。
- 文件路径：OSS 上文件的路径。例如：`bucket-name/path/to/your/file.csv`。

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/conn_oss.png)

#### 标准 S3

要将兼容 S3 协议的对象存储服务（如 AWS S3、MinIO 等）中的文件导入至 MatrixOne Intelligence 平台，您需提供以下连接配置信息：

- Endpoint: 标准 S3 服务的访问地址。例如：`https://s3.amazonaws.com`。
- AccessKeyId: 您的标准 S3 账号的 AccessKey ID。
- AccessKeySecret: 您的标准 S3 账号的 AccessKey Secret。
- 文件路径：S3 上文件的路径。例如：`bucket-name/path/to/your/file.csv`。
- S3 地址风格：S3 地址风格决定了访问存储桶（Bucket）的 URL 结构，虚拟主机风格（Virtual Host）（推荐）：https: //my-bucket.s3.amazonaws.com/my-object，路径风格（Path Style）（部分旧系统）：https: //s3.amazonaws.com/my-bucket/my-object，AWS 目前推荐使用虚拟主机风格，部分私有 S3 兼容存储（如 MinIO）仍可能需要路径风格。
- 地区：S3 存储桶所在的地区。例如：us-east-1。

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/conn_s3.png)

### 分布式文件系统

#### HDFS

要将 HDFS 中的文件导入至 MatrixOne Intelligence 平台，您需要提供以下连接配置信息以完成数据接入配置：

- HDFS 地址：如 `hdfs://namenode:9000`
- 认证方式：支持 Simple 和 Kerberos 两种认证方法
- Simple
    - HDFS 用户名：HDFS 访问用户名
    - 文件路径：HDFS 文件路径
- Kerberos
    - Kerberos Principal：Kerberos 中用于标识用户或服务的主体（Principal），客户端通过它向 Kerberos 认证服务请求票据，从而证明身份。
    - Keytab 文件：存储 Kerberos 主体和加密密钥的文件，通常用于自动化认证，客户端可以使用它向 Kerberos 获取票据而无需手动输入密码，需要妥善保管。
    - Krb5 配置文件：Kerberos 客户端配置文件，定义了 Realm、KDC 等信息，告诉客户端如何与 Kerberos 服务器交互进行身份验证。
    - 代理用户：在某些场景下，Kerberos 认证主体需要以其他用户身份访问 HDFS，可指定代理用户以实现权限委托，让主用户代表代理用户执行操作，如果不使用代理用户可以留空。
    - 文件路径：HDFS 文件路径

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/hdfs.png)

**连接问题排查**:

如果出现连接错误 (`service: new connector by config err: failed to create hdfs client: no available namenodes: dial tcp 43.139.183.124:9000: i/o timeout"`)，请检查：

1. **端口开放**:

确保以下端口在网络环境中已开放：
	·	NameNode 默认端口：9000
	·	DataNode 默认端口：9866

如使用了非默认端口，请相应开放对应端口。

2. **Hadoop 配置**:

检查 core-site.xml 和 hdfs-site.xml 配置文件是否包含如下配置：

core-site.xml 中 hdfs://10.1.19.23:9000 为主机 namenode 的内网 IP 地址。端口 9000 是 HDFS NameNode 的默认端口

```xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://10.1.19.23:9000</value>
    </property>
    <property>
        <name>hadoop.tmp.dir</name>
        <value>/home/hadoop/hdfs/tmp</value>
    </property>
</configuration>
```

hdfs-site.xml 中 dfs.datanode.hostname 为 DataNode 的公网 IP（47.111.156.240），需在 hdfs-site.xml 中添加配置 dfs.datanode.hostname，强制 DataNode 报告公网 IP 47.111.156.240。

```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
    <property>
        <name>dfs.namenode.name.dir</name>
        <value>file:///home/hadoop/hdfs/namenode</value>
    </property>
    <property>
        <name>dfs.datanode.data.dir</name>
        <value>file:///home/hadoop/hdfs/datanode</value>
    </property>
    <property>
        <name>dfs.datanode.hostname</name>
        <value>47.111.156.240</value>
    </property>
</configuration>
```

3. **主机名绑定**:
  
检查主机名（/etc/hosts）是否绑定的是内网 ip，避免使用公网 ip 绑定，例如以下主机名 iZbp14hbhigjmqticskavqZ 映射到内网 IP

```bash
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6
10.1.19.23  iZbp14hbhigjmqticskavqZ
```
  
### 数据库

#### MatrixOne

要将处理好的文件导出到 MatrixOne 知识库，需要提供数据库连接信息，包括主机、端口、用户名、密码。

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/conn_mo.png)

### 知识库

#### Dify

要将处理好的文件导出到 Dify 知识库，需要提供 API URL 和 API Key，具体配置方法请参考[数据导出](./export.md)

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/dify_conn.png)