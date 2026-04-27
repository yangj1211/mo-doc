# Serverless 生产实例价格明细

## CU

Compute Unit（简称 CU）是 MatrixOne Intelligence Serverless 实例的计算资源开销的基本单位，每个 SQL 查询都会消耗一定数量的 CU，它包含 CPU、Memory、对象存储 I/O 和公网流量的消耗量。

我们定义 1 个 CU 计算资源消耗量 = MO 读取 32KB 数据所消耗的计算资源。以下为 CU 消费数量与其包含资源的对应信息：

<table>
  <tr>
    <th>类型</th>
    <th>消耗量</th>
    <th>消费 CU 数</th>
  </tr>
  <tr>
    <td >CPU</td>
    <td>1 ms*core</td>
    <td>0.052</td>
  </tr>
  <tr>
    <td >Memory</td>
    <td>1 GB*s </td>
    <td>10.9 </td>
  </tr>
  <tr>
    <td >Network（公网）</td>
    <td>1 KB Network egress</td>
    <td> 0.74</td>
  </tr>
  <tr>
    <td> Network（私网）</td>
    <td>1 KB Network egress</td>
    <td>0</td>
  </tr>
  <tr>
    <td rowspan="2" style="vertical-align: middle;">Storage I/O</td>
    <td>1 storage read request </td>
    <td> 0.97 </td>
  </tr>
  <tr>
    <td>1 storage write request</td>
    <td>0.97</td>
  </tr>
</table>

目前，MO Intelligence 的 CU 定价为 **¥1/10 万-CUs**。

## 存储

数据存储是指用户在 MatrixOne Intelligence 实例中存入的数据大小，MO Intelligence 的存储定价为 **¥0.15/GiB-月**。