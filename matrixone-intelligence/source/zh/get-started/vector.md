# 快速上手向量能力

本文介绍了 MatrixOne Intelligence 向量数据特征及在相关领域的应用，旨在为用户提供一个入门级别的最佳实践指引。

## 什么是向量？

在数据库中，向量通常表示为一个一维数组或列表，其中每个元素是一个浮点数或整数。向量可以表示各种类型的数据，如文本、图像、音频等，通过特征提取技术将这些数据转换为向量。

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/docs/reference/vector/vector_introduction.png width=80% heigth=80%/>
</div>

## 应用场景

- 自然语言处理：在文本数据库中，向量表示可以用于表示文本或词语的语义。通过词嵌入技术，每个单词或文档都可以被表示为向量，数据库可以基于这些向量进行高效的语义搜索或分类。
- 推荐系统：向量用于在推荐系统中表示用户和物品。通过计算用户向量与物品向量之间的相似性，可以生成个性化的推荐列表。
- 聚类和分类：向量在数据库中也用于聚类和分类任务。数据库系统可以根据向量之间的相似性对数据进行自动分组或分类，以发现数据中的潜在模式和关系。
- 多模态数据处理：向量表示也广泛应用于处理多模态数据，即结合不同类型数据（如图像、文本、音频）的场景。向量化表示使得不同模态的数据可以在同一空间中进行比较和计算。

## 相关概念

- 向量类型：在数据库中，向量类型通常指的是用于表示和存储向量的专用数据类型。
- 向量检索：向量检索是一种通过比较向量之间的相似性的检索，它利用距离度量算法来查找与给定查询向量最相似的向量。常用的距离度量有欧几里得距离（L2 distance)、余弦相似度、内积等。区别与传统数据库检索，传统数据库上的标量搜索主要针对结构化数据进行精确的数据查询，而向量搜索主要针对非结构化数据向量化之后的向量数据进行相似检索，只能近似获得最匹配的结果。

    <div align="center">
    <img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/get-started/vecter-vs-scale.png width=80% heigth=80%/>
    </div>

    - 在标量数据库中存储的是原始数据。例如，用户数据可能以表格形式保存，包括字段如姓名、年龄等。中执行查询返回的是精确匹配的结果。例如，查询 name = 'tom' 的年龄时得到精确返回。
    - 在向量数据库中存储的是经过处理后的向量数据（通常是 Embedding 向量）。这些向量代表了数据在高维空间中的位置，用于进行相似度检索。这种查询会返回与给定向量最相似的记录，通常以 Top K 的形式返回最相似的几个结果。返回的是相似的结果，而不是精确匹配。例如，将表中的向量与 "[1,2,1]" 这个向量对比，返回与给定向量最相似的一内容，即 [content=pears]。

- 向量索引：向量索引是一种专门用于处理向量数据的索引技术，旨在提高高维向量数据的检索效率，它允许数据库在大规模数据集中快速找到与查询向量最相似的向量。

### 向量类型

在 MatrixOne Intelligence 中，向量被定义为一种特殊的一维数据类型，类似于编程中的数组，但目前仅支持 float32 和 float64 两种数值类型，分别表示为 vecf32 和 vecf64。创建向量列时，可以指定其维度，例如 vecf32(3)，这表示向量的长度为 3，最大支持达到 65,535 维，而不支持字符串或整型。

```sql
create table t1(a int, b vecf32(3), c vecf64(3))
insert into t1 values(1, "[1,2,3]", "[4,5,6]");
mysql> select * from t1;
+------+-----------+-----------+
| a    | b         | c         |
+------+-----------+-----------+
|    1 | [1, 2, 3] | [4, 5, 6] |
+------+-----------+-----------+
1 row in set (0.01 sec)
```

### 向量检索

MatrixOne Intelligence 支持多种向量相似度函数，如常见余弦相似度，欧几里得距离和内积等。

```sql
create table vec_table(a int, b vecf32(3), c vecf64(3));
insert into vec_table values(1, "[1,2,3]", "[4,5,6]");

-- 1. 使用余弦相似度函数进行相似度检索
mysql> select cosine_similarity(b,"[1,5,6]") from vec_table;
+-------------------------------+
| cosine_similarity(b, [1,5,6]) |
+-------------------------------+
|            0.9843241382880896 |
+-------------------------------+
1 row in set (0.00 sec)

-- 2. 使用欧几里得距离函数进行相似度检索
mysql> select l2_distance(b,"[1,5,6]") from vec_table;
+-------------------------+
| l2_distance(b, [1,5,6]) |
+-------------------------+
|       4.242640687119285 |
+-------------------------+
1 row in set (0.01 sec)

-- 3. 使用内积函数进行相似度检索
mysql> select inner_product(b,"[1,5,6]") from vec_table;
+---------------------------+
| inner_product(b, [1,5,6]) |
+---------------------------+
|                        29 |
+---------------------------+
1 row in set (0.00 sec)
```

### 向量索引

向量索引可以在大规模数据集中高效地查找和检索相似向量。目前，MatrixOne Intelligence 支持使用欧几里得距离度量的 IVFFLAT 类型的向量索引。

```sql
create table vec_table(a int, b vecf32(3), c vecf64(3));
insert into vec_table values(1, "[1,2,3]", "[4,5,6]");

#需设置参数 experimental_ivf_index 值为 1（默认 0）才能使用向量索引，重新连接数据库生效
SET GLOBAL experimental_ivf_index = 1;

#在向量列创建向量索引，设定分区数为1，使用欧几里得距离度量。
create index ivf_idx1 using ivfflat on vec_table(b)  lists=1 op_type "vector_l2_ops";
```

## 应用示例：构建 RAG 应用

RAG，全称为 Retrieval-Augmented Generation（检索增强生成），是一种结合了信息检索和文本生成的技术，用于提高大型语言模型（LLM）生成文本的准确性和相关性。LLM 由于其训练数据的局限性，可能无法获取最新的信息。
RAG 的工作流程通常包括以下几个步骤：

- 检索（Retrieve）：从大型数据集或知识库中查找并提取与当前查询最相关的信息。
- 增强（Augment）：将检索到的信息或数据集与 LLM 结合，以增强 LLM 的性能和输出的准确性。
- 生成（Generate）：使用检索到的信息利用 LLM 来生成新的文本或响应。

<div align="center">
<img src=https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/get-started/rag.png width=80% heigth=80%/>
</div>

Matrxione 作为超融合数据库，自带向量能力，这在 RAG 应用中起着重要的作用。以下我们利用 MatrixOne Intelligence 的向量能力快速构建一个 Native RAG 应用。

### 前置依赖

- 已完成 Python 3.8(or plus) version 安装
- 已完成 MySQL 客户端安装
- 下载安装 pymysql 工具

```bash
pip install pymysql
```

- 已在 [Neolink.ai](https://Neolink.AI) 上获取 api key，Neolink.AI 是一款全面链接算力、数据、知识、模型与企业应用的平台。

### 操作步骤

**步骤一：**建表并开启向量索引

连接 MatrixOne Intelligence，建立一个名为 rag_tab 的表来存储文本信息和对应的向量信息，然后开启向量索引。

```sql
create table rag_tab(content text,embedding vecf32(1024));
#重新连接数据库生效
SET GLOBAL experimental_ivf_index = 1;
```

**步骤二：**构建应用

创建 python 文件 rag_example.py，写入以下内容。该脚本主要作用是利用 mxbai-embed-large 嵌入模型将文本进行向量化，然后存到 MatrixOne Intelligence 表中。然后把问题也进行向量化，利用 MatrixOne Intelligence 的向量检索找出最相似的文本块，最后结合大语言模型 llama2 得出答案。

```sql
vi ./rag_example.py
```

```python
import time
import requests
import pymysql

conn = pymysql.connect(
        host = 'freetier-01.cn-hangzhou.cluster.matrixonecloud.cn',
        port = 6001,
        user = '585b49fc_852b_4bd1_b6d1_d64bc1d8xxxx:admin:accountadmin',
        password = "xxx",
        db = 'db1',
        autocommit = True
        )

cursor = conn.cursor()

api_key='0e972228-0b50-442d-b74c-73f43314xxxx' # 将 api 修改为您的个人 key
api_url_llm = "https://neolink-ai.com/model/api/v1/chat/completions"
api_url_emb="https://neolink-ai.com/model/api/v1/embeddings"
# 使用 neolink-ai 的在线 llm 和 embedding 模型

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

documents = [
"MatrixOne is a hyper-converged cloud & edge native distributed database with a structure that separates storage, computation, and transactions to form a consolidated HSTAP data engine. This engine enables a single database system to accommodate diverse business loads such as OLTP, OLAP, and stream computing. It also supports deployment and utilization across public, private, and edge clouds, ensuring compatibility with diverse infrastructures.",
"MatrixOne touts significant features, including real-time HTAP, multi-tenancy, stream computation, extreme scalability, cost-effectiveness, enterprise-grade availability, and extensive MySQL compatibility. MatrixOne unifies tasks traditionally performed by multiple databases into one system by offering a comprehensive ultra-hybrid data solution. This consolidation simplifies development and operations, minimizes data fragmentation, and boosts development agility.",
"MatrixOne is optimally suited for scenarios requiring real-time data input, large data scales, frequent load fluctuations, and a mix of procedural and analytical business operations. It caters to use cases such as mobile internet apps, IoT data applications, real-time data warehouses, SaaS platforms, and more.",
"Matrix is a collection of complex or real numbers arranged in a rectangular array.",
]

#文本分块并向量化存入 MO
for i,d in enumerate(documents):
    emb_data = {
        "input": d,
        "model": "BAAI/bge-m3"
    }
    response = requests.post(api_url_emb, headers=headers, json=emb_data)
    embedding = response.json().get('data')[0].get('embedding')
    insert_sql = "insert into rag_tab(content,embedding) values (%s, %s)"
    data_to_insert = (d, str(embedding))
    cursor.execute(insert_sql, data_to_insert)

#创建索引
create_sql = 'create index idx_rag using ivfflat on rag_tab(embedding) lists=%s op_type "vector_l2_ops"'
cursor.execute(create_sql, 1)

#提问
prompt = "What is MatrixOne?"

#问题向量化，与数据库向量进行相似度搜索
emb_data = {
        "input": prompt,
        "model": "BAAI/bge-m3"
    }
response_emb = requests.post(api_url_emb, headers=headers, json=emb_data)

query_embedding= response.json().get('data')[0].get('embedding')
query_sql = "select content from rag_tab order by l2_distance(embedding,%s) asc limit 3"
data_to_query = str(query_embedding)
cursor.execute(query_sql, data_to_query)
data = cursor.fetchall()

#使用 LLM 模型结合数据库检索结果返回回答
llm_data = {
    "model": "meta-llama/Meta-Llama-3.1-405B-Instruct-FP8",
    "messages": [
        {
            "role": "system",
            "content": str(data)
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
}

response_llm = requests.post(api_url_llm, headers=headers, json=llm_data)

response_data = response_llm.json()
answer = response_data['choices'][0]['message']['content']

print(answer)
```

### 执行脚本

```bash
python ./rag_example_2.py
```

```bash
MatrixOne is a hyper-converged cloud & edge native distributed database. It has a structure that separates storage, computation, and transactions to form a consolidated HSTAP (Hybrid Transactional/Analytical Processing) data engine. This engine enables a single database system to accommodate diverse business loads such as OLTP (Online Transactional Processing), OLAP (Online Analytical Processing), and stream computing.
```