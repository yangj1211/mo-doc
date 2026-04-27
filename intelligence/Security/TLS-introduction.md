# 数据传输加密

MatrixOne Intelligence 采用默认的加密传输，支持 TLS 协议的加密传输，通过该方式减少了数据库中敏感信息泄露的风险。加密传输是一种通过密钥对信息进行加密和解密的方法，有助于有效保护数据的安全。

传输层安全性（Transport Layer Security，TLS）是一种广泛采用的安全协议，MatrixOne Intelligence 支持多个协议版本，包括 TLS 1.0、TLS 1.1 和 TLS 1.2。

## 如何使用

### 1. 验证 MatrixOne Intelligence 的 SSL 是否启用

1. 登录到 MatrixOne Intelligence，选择目标实例，点击**连接 > 通过第三方工具连接**，右侧滑窗内可查阅到 MatrixOne Intelligence 上你的实例连接串。

2. 使用 MySQL 客户端连接 MatrixOne Intelligence 实例：

    ```
    mysql -h host_ip_address -P 6001 -u <accountname>:<username>:<rolename>  -p

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
    ```

    上述代码段显示，你已连接成功。

3. 使用 `Status` 命令查看 SSL 是否启用。

    成功启用，代码示例如下所示，可以看到 SSL 状态为 `Cipher in use is TLS_AES_128_GCM_SHA256`：

    ```
    mysql> status
    --------------
    mysql  Ver 8.1.0 for macos11.7 on arm64 (Homebrew)

    Connection id:  13560771
    Current database:
    Current user:  admin@localhost
    SSL:   Cipher in use is TLS_AES_128_GCM_SHA256
    Current pager:  less
    Using outfile:  ''
    Using delimiter: ;
    Server version:  8.0.30-MatrixOne-v2.0.3 MatrixOne
    Protocol version: 10
    Connection:  freetier-01.cn-hangzhou.cluster.matrixonecloud.cn via TCP/IP
    Server characterset: utf8mb4
    Db     characterset: utf8mb4
    Client characterset: utf8mb4
    Conn.  characterset: utf8mb4
    TCP port:  6001
    Binary data as:  Hexadecimal
    --------------
    ```

### 2. 配置 MySQL 客户端参数

你也可以在通过 MySQL 客户端连接 MatrixOne Intelligence 时，通过 `--ssl-mode` 参数指定加密连接行为，代码示例如下：

```sql
mysql -h host_ip_address -P 6001 -u <accountname>:<username>:<rolename>  -p --ssl-mode=PREFERRED
```

ssl-mode 取值类型如下：

|ssl-mode 取值 | 含义|
|---|---|
|DISABLED|不使用 SSL/TLS 建立加密连接，与 skip-ssl 同义。|
|PREFERRED|默认行为，优先尝试使用 SSL/TLS 建立加密连接，如果无法建则尝试建立非 SSL/TLS 连接。|
|REQUIRED|只会尝试使用 SSL/TLS 建立加密连接，如果无法建立连接，则会连接失败。|
|VERIFY_CA|与 REQUIRED 行为一样，并且还会验证 Server 端的 CA 证书是否有效。|
|VERIFY_IDENTITY|与 VERIFY_CA 行为一样，并且还验证 Server 端 CA 证书中的 host 是否与实际连接的 hostname 是否一致。|

:::{note}
客户端在指定了 `--ssl-mode=VERIFY_CA` 时，需要使用 `--ssl-ca` 来指定 CA 证书。
客户端在指定了 `--ssl-mode=VERIFY_IDENTITY` 时，需要指定 CA 证书，且需要使用 `--ssl-key` 指定客户端的私钥和使用 `--ssl-cert` 指定客户端的证书。
:::