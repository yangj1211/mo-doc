# 数据中心

数据中心是统一的数据存储与管理枢纽，面向多模态数据场景进行设计，支持对结构化与非结构化数据的高效存储与组织，满足数据驱动业务在规模化、稳定性与可管理性方面的需求。同时，数据中心支持直接订阅来自 MatrixOne 实例的数据库表，实现业务数据的集中汇聚与持续同步，为分析、建模及智能应用提供可靠的数据基础。

## 数据组织结构说明

MOI 平台采用三级结构进行数据管理：**目录 → 库 → 卷**，以实现灵活、可控的数据隔离与组织。

- **目录**  
  数据治理的最高层级单位，通常代表一个数据隔离区或生命周期阶段，如：生产目录、开发目录、非客户数据目录、敏感数据目录等，每个目录内的数据相互隔离，适用于权限分级和合规管理。

- **库**  
  目录下的数据分类单元，用于组织结构化或非结构化数据资源。一个目录中可包含多个库，便于按业务维度、数据类型或处理阶段细化管理。

- **卷**  
  库下的存储单元，主要用于管理非表格类文件（如 PDF、图片、音频等）。卷是面向文件系统的逻辑容器。

每个工作区初始化时，系统会自动创建以下两个目录：

- **系统目录**  
  用于存储平台运行过程中的系统数据，仅管理员可见和访问。

- **默认目录**  
  为用户快速上手而预置的目录，不可以修改和删除，包含两个默认库：

  - **原始数据**：不能修改和删除，用于存放用户上传的原始文件或数据，并内置样例数据卷存放工作流模版的样例数据。
  - **处理数据**：不能修改和删除，用于存放经过清洗、解析、提取等处理后的数据成果

## 非结构化数据

### 结果展示

点击文件列表右侧的预览按钮可查看该文件的血缘信息。

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/data_lineage_1.png)

### 结果下载

点击下载后，根据不同的最终节点，将下载不同的处理结果，处理结果是一个 zip，文件夹。

<table border="1" cellpadding="6" cellspacing="0">
  <thead>
    <tr>
      <th>文件类型</th>
      <th>最终处理节点</th>
      <th>下载文件组成</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="4">文档</td>
      <td>• 文档解析节点<br>• 数据清洗节点<br>• 分段节点</td>
      <td>• json 文件（解析结果）<br>• md 文件（存放完整的解析后 markdown 内容）<br>• images 文件夹（存放解析生成的图片资源）<br>• tables 文件夹（存放解析生成的表格资源）</td>
    </tr>
    <tr>
      <td>• 文本嵌入节点</td>
      <td>• json 文件（解析结果）<br>• md 文件（存放完整的解析后 markdown 内容）<br>• images 文件夹（存放解析生成的图片资源）<br>• tables 文件夹（存放解析生成的表格资源）<br>• json 文件（包含 embedding 信息）</td>
    </tr>
    <tr>
      <td>• 信息提取节点（原结构化提取节点）</td>
      <td><strong>经过解析节点：</strong><br>• json 文件（提取）<br>• md 文件（存放完整的解析后 markdown 内容）<br>• images 文件夹（存放解析生成的图片资源）<br>• tables 文件夹（存放解析生成的表格资源）<br><br><strong>不经过解析节点：</strong><br>• json 文件（提取结果）<br>• tables 文件夹（存放解析生成的表格资源）</td>
    </tr>
    <tr>
      <td>• 数据增强节点</td>
      <td><strong>经过解析节点：</strong><br>• jsonl 文件 (存放增强生成的 QA 对)<br>• md 文件（存放完整的解析后 markdown 内容）<br>• images 文件夹（存放解析生成的图片资源）<br>• tables 文件夹（存放解析生成的表格资源）<br><br><strong>不经过解析节点：</strong><br>• jsonl 文件</td>
    </tr>
    <tr>
      <td rowspan="4">图片</td>
      <td>• 图片解析节点<br>• 数据清洗节点<br>• 分段节点</td>
      <td>• json 文件（解析结果）<br>• images 文件夹</td>
    </tr>
    <tr>
      <td>• 文本嵌入节点</td>
      <td>• json 文件（解析结果）<br>• images 文件夹（存放解析生成的图片资源）<br>• json 文件（含 embedding）</td>
    </tr>
    <tr>
      <td>• 信息提取节点</td>
      <td><strong>经过解析节点：</strong><br>• json 文件（提取结果）<br>• images 文件夹（存放解析生成的图片资源）<br>• tables 文件夹（存放提取生成的表格）<br><br><strong>不经过解析节点：</strong><br>• json 文件（提取结果）<br>• tables 文件夹（存放提取生成的表格）</td>
    </tr>
    <tr>
      <td>• 数据增强节点</td>
      <td><strong>经过解析节点：</strong><br>• jsonl 文件 (存放增强生成的 QA 对)<br>• md 文件（存放完整的解析后 markdown 内容）<br>• images 文件夹（存放解析生成的图片资源）<br>• tables 文件夹（存放解析生成的表格资源）<br><br><strong>不经过解析节点：</strong><br>• jsonl 文件 (存放增强生成的 QA 对)</td>
    </tr>
    <tr>
      <td rowspan="4">音频/视频</td>
      <td>• 音频解析节点 / 视频解析节点<br>• 数据清洗节点<br>• 分段节点 </td>
      <td>• json 文件（解析结果）</td>
    </tr>
    <tr>
      <td>• 文本嵌入节点</td>
      <td>• json 文件（解析结果）<br>• json 文件（含 embedding）</td>
    </tr>
    <tr>
      <td>• 信息提取节点</td>
      <td>• json 文件（提取结果）<br>• tables 文件夹（存放提取生成的表格）</td>
    </tr>
    <tr>
      <td>• 数据增强节点</td>
      <td>• jsonl 文件 (存放增强生成的 QA 对)</td>
    </tr>
  </tbody>
</table>

## 结构化数据

### 结果展示

点击表名可以查看表的详情信息，包括行列信息，建表语句、抽样数据等。

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/table_1.png)

### 结果下载

点击右侧的下载按钮可将表数据导出为 csv 文件

![](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/table_2.png)
