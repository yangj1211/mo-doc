# 导入对象存储数据

本章将详细介绍如何将存储在公有云上的对象存储数据文件导入到 MatrixOne 实例中。

## 导入前检查

在进行数据导入之前，确保您已经检查并了解了以下数据文件信息。

### 对象存储服务

MatrixOne Intelligence 支持多种云厂商的对象存储服务，包括：

| 云厂商  | 对象存储名称 |
| ------- | -------------- |
| AWS     | S3             |
| 阿里云  | OSS            |

### 数据文件类型

MatrixOne 支持从对象存储服务批量导入以下数据文件类型：

- **CSV 文件**：适合结构化数据。
- **JSONLines 文件**：一种方便存储结构化数据的格式，也称为换行符分隔的 JSON。

#### 关于 JSONLines 格式

JSON（JavaScript Object Notation）是一种轻量级的数据交换格式，而 JSONLines 是一种更为方便存储结构化数据的格式，它采用换行符作为分隔符，每行都包含独立、完整且合法的 JSON 值。这种格式适合处理数据流，因为每行都代表一个单独的条目，可以轻松流式传输，无需自定义解析器。请注意，MatrixOne 对 JSONLines 格式的要求较为严格，只允许包含相同类型值和普通结构的 JSON 对象或 JSON 数组。如果 JSONLines 文件具有嵌套结构，MatrixOne 目前不支持加载它。

以下是 JSONLines 格式的示例：

**有效 JSONLines 对象示例：**

```json
{"id": 1, "father": "Mark", "mother": "Charlotte"}
{"id": 2, "father": "John", "mother": "Ann"}
{"id": 3, "father": "Bob", "mother": "Monika"}
```

**无效 JSONLines 对象示例（具有嵌套结构）：**

```json
{"id": 1, "father": "Mark", "mother": "Charlotte", "children": ["Tom"]}
{"id": 2, "father": "John", "mother": "Ann", "children": ["Jessika", "Antony", "Jack"]}
{"id": 3, "father": "Bob", "mother": "Monika", "children": ["Jerry", "Karol"]}
```

**有效 JSONLines 数组示例（类似于 CSV 格式）：**

```json
["Name", "Session", "Score", "Completed"]
["Gilbert", "2013", 24, true]
["Alexa", "2013", 29, true]
["May", "2012B", 14, false]
["Deloise", "2012A", 19, true]
```

**无效 JSONLines 数组示例（因数据类型和列数不匹配而无效）：**

```json
["Gilbert", "2013", 24, true, 100]
["Alexa", "2013", "twenty nine", true]
["May", "2012B", 14, "no"]
["Deloise", "2012A", 19, true, 40]
```

由于 JSON 数据类型与 MatrixOne 的数据类型不同，因此在导入 JSONLines 文件之前，需要先创建数据表并确保其数据类型与文件中的数据类型匹配。

## 导入方式

MatrixOne 提供了多种方式来导入对象存储数据文件。以下是其中两种主要方式的详细描述。

### Web UI 互动引导

MatrixOne Intelligence 提供了界面化的引导方式，使数据导入变得简单。以下是使用 Web UI 进行数据导入的步骤：

#### 步骤一：打开导入窗口

在 SQL 编辑器功能中，单击 "导入" 按钮，如下图所示：

![打开导入窗口](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/import/s3/s3-1.png)

#### 步骤二：选择文件所在的对象存储

点击 "导入你的数据"，并选择要导入的对象存储服务，如下图所示：

![选择对象存储服务](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/import/s3/s3-2.png)

#### 步骤三：选择数据文件格式

对于 **CSV 文件格式**，您可以根据文件结构选择适当的字段分隔符和字段包围符。默认的字段分隔符是逗号（","），字段包围符是回车和换行符（"\r\n"），如下图所示：

![选择 CSV 文件格式](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/import/s3/s3-3.png)

#### 步骤四：填写数据文件地址

将数据文件的路径填入相应框中，并指定文件的地区。请注意，选择错误的文件地区可能导致导入失败，如下图所示：

![填写数据文件地址](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/import/s3/s3-4.png)

#### 步骤五：填写安全认证方式

MatrixOne Intelligence 支持两种安全认证方式，即访问密钥和角色 ARN，用于访问导入的数据源。

**访问密钥：**

- **AWS**：填写 IAM 用户的 Access Key 和 Secret Access，该用户必须具有访问导入数据的权限。
- **阿里云**：填写 RAM 用户的 AccessKey ID 和 AccessKey Secret，该用户必须具有访问导入数据的权限，如下图所示：

![填写访问密钥](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/import/s3/s3-5.png)

#### 步骤六：选择导入的数据表

指定对象存储中的数据源以及 MatrixOne 实例中的数据库和数据表，然后完成数据导入。

### SQL 语句导入

使用 SQL 语句执行数据文件的导入是一种经典且常用的数据导入方式。MatrixOne 支持使用 `LOAD DATA` 语句来导入对象存储数据文件。

#### 导入 CSV 文件

**语法结构：**

```sql
LOAD DATA URL s3options {
    "provider" = '<string>',
    "endpoint" = '<string>',
    "bucket" = '<string>',
    "access_key_id" = '<string>',
    "secret_access_key" = '<string>',
    "role_arn" = 'xxxx',
    "external_id" = 'yyy',
    "filepath" = '<string>',
    "format" = 'csv',
    "compression" = '<string>'
}
INTO TABLE tbl_name
[{
    FIELDS | COLUMNS
    [TERMINATED BY '<string>']
    [[OPTIONALLY] ENCLOSED BY '<string>']
}]
[LINES
    [STARTING BY 'string']
    [TERMINATED BY 'string']
]
[IGNORE number {LINES | ROWS}]
[PARALLEL {'TRUE' | 'FALSE'}]
```

**参数说明：**

- `provider`：对象存储所在的公有云，例如 AWS 或阿里云。如果不填写，默认是 AWS。
- `endpoint`：OSS 的访问域名，例如 oss-cn-hangzhou.internal.aliyuncs.com。对于阿里云，此参数必填；对于 AWS，无需填写。
- `bucket`：数据所在的存储桶。
- `access_key_id`：AccessKey ID（可选）。
- `secret_access_key`：AccessKey Secret（可选）。
- `role_arn`：RAM 角色的 ARN（可选）。
- `external_id`：（可选）
- `file_path`：完整的对象存储文件路径，例如 mocloud_sampledata/tpch-sf1/lineitems.csv。
- `format`：对象存储文件格式，默认是 CSV。
- `compression`：对象存储文件的压缩格式，如果不填写或值为 "none"。

注意：本方法用于导入 CSV 文件。

**语法示例**

**使用 AK/SK 的认证方式加载 AWS S3 上的数据：**

```sql
LOAD DATA URL s3options {
    "bucket" = 'test-load-mo',
    "access_key_id" = 'XXXXXX',
    "secret_access_key" = 'XXXXXX',
    "filepath" = 'mo_test/test.csv'
}
INTO TABLE t1
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n';
```

**使用 Role ARN 的认证方式加载阿里云 OSS 上的数据：**

```sql
LOAD DATA URL s3options {
    "provider" = 'aliyun',
    "endpoint" = 'oss-cn-hangzhou-internal.aliyuncs.com',
    "bucket" = 'test-load-data',
    "role_arn" = 'xxxxxxx',
    "external_id" = 'xxxxx',
    "filepath" = 'mo_test/test.csv'
}
INTO TABLE t1
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\n';
```

#### 导入 JSONLines 文件

**语法结构：**

```sql
LOAD DATA URL s3options {
    "provider" = '<string>',
    "endpoint" = '<string>',
    "bucket" = '<string>',
    "access_key_id" = '<string>',
    "secret_access_key" = '<string>',
    "role_arn" = 'xxxx',
    "external_id" = 'yyy',
    "filepath" = '<string>',
    "format" = 'jsonline',
    'jsondata' = '<string>',
    "compression" = '<string>'
}
INTO TABLE tbl_name
[IGNORE number {LINES | ROWS}]
[PARALLEL {'TRUE' | 'FALSE'}]
```

**参数说明：**

- `provider`：对象存储所在的公有云，例如 AWS 或阿里云

。如果不填写，默认是 AWS。

- `endpoint`：OSS 的访问域名，例如 oss-cn-hangzhou.internal.aliyuncs.com。对于阿里云，此参数必填；对于 AWS，无需填写。
- `bucket`：数据所在的存储桶。
- `access_key_id`：AccessKey ID（可选）。
- `secret_access_key`：AccessKey Secret（可选）。
- `role_arn`：RAM 角色的 ARN（可选）。
- `external_id`：（可选）
- `file_path`：完整的对象存储文件路径，例如 mocloud_sampledata/tpch-sf1/lineitems.csv。
- `format`：对象存储文件格式，必须填写为 "jsonline"。
- `jsondata`：JSON 数据格式（可选）。
- `compression`：对象存储文件的压缩格式，如果不填写或值为 "none"。

注意：本方法用于导入 JSONLines 文件。

**语法示例**

**使用 AK/SK 的认证方式加载 AWS S3 上的数据：**

```sql
LOAD DATA URL s3options {
    "bucket" = 'test-load-mo',
    "access_key_id" = 'XXXXXX',
    "secret_access_key" = 'XXXXXX',
    "format" = 'jsonline',
    "jsondata" = 'array',
    "filepath" = 'mo_test/test.csv'
}
INTO TABLE t1;
```

**使用 Role ARN 的认证方式加载阿里云 OSS 上的数据：**

```sql
LOAD DATA URL s3options {
    "provider" = 'aliyun',
    "endpoint" = 'oss-cn-hangzhou-internal.aliyuncs.com',
    "bucket" = 'test-load-data',
    "role_arn" = 'xxxxxxx',
    "external_id" = 'xxxxx',
    "filepath" = 'mo_test/test.csv',
    "format" = 'jsonline',
    "jsondata" = 'array'
}
INTO TABLE t1;
```

### 安全认证

访问公有云的对象存储文件时，需要进行安全认证以确保数据的安全性和完整性。用户使用 MatrixOne 实例访问自己的对象存储文件时可以使用访问密钥和角色 ARN 两种安全认证方式。您可以选择其中一种方式，并在公有云账户中进行配置。在导入数据时，只需填写其中一种认证方式的参数，包括 `access_key_id`、`secret_access_key`、`role_arn` 和 `external_id`。

#### 访问密钥

访问密钥由一组标识用户的访问密钥 ID 和密钥组成。在 `LOAD DATA` 语句中，它们分别对应 `access_key_id` 和 `secret_access_key` 字段。请确保提供的访问密钥用户具有访问要导入的对象存储文件的读取权限。

##### **AWS**

建议使用 IAM 用户（而不是 AWS 账户的根用户）创建访问密钥。具体步骤如下：

1. 创建 IAM 用户，并为该用户分配源数据存储桶的 `AmazonS3ReadOnlyAccess` 策略，以及 `CreateOwnAccessKeys` 和 `ManageOwnAccessKeys` 的策略。详情请参阅[创建 IAM 用户](https://docs.aws.amazon.com/zh_cn/IAM/latest/UserGuide/id_users_create.html#id_users_create_console)。
2. 使用 IAM 用户登录 [IAM 控制台](https://console.aws.amazon.com/iam)。
3. 创建访问密钥。详情请参阅[管理访问密钥](https://docs.aws.amazon.com/zh_cn/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey)。

##### **阿里云**

建议使用 RAM 用户（而不是阿里云账户的根用户）创建访问密钥。具体步骤如下：

1. 创建 RAM 用户，并为该用户分配源数据存储桶的 `AliyunOSSReadOnlyAccess` 策略。详情请参阅[创建 RAM 用户](https://help.aliyun.com/zh/ram/user-guide/create-a-ram-user?spm=a2c4g.11174283.0.0.40572230YxfiT6)。
2. 使用 RAM 用户登录 [RAM 控制台](https://ram.console.aliyun.com/overview)。
3. 创建访问密钥。详情请参阅[创建访问密钥](https://help.aliyun.com/zh/ram/user-guide/create-an-accesskey-pair?spm=a2c4g.11186623.0.0.50452230cq6Dt0)。

:::{note}
阿里云的 `AccessKey Secret` 对应 `secret_access_key` 字段。
:::