# 使用指南

本文档面向内容作者和开发者，介绍如何在本项目中添加、编辑和构建文档。

---

## 1. 项目简介

这是一个基于 **Sphinx + MyST + Furo** 的多产品文档站，支持中英双语，目前包含两个产品：

| 产品 | 目录 | 中文 | 英文 |
|---|---|---|---|
| MatrixOne（数据库） | `matrixone/` | 全量 | 全量 |
| MatrixOne Intelligence（AI 平台） | `matrixone-intelligence/` | 全量（479 篇） | 部分（5 篇核心） |

每个产品是一个独立的子项目，拥有自己的 `conf.py`、`Makefile` 和 `source/` 目录。中英文内容分别放在 `source/zh/` 和 `source/en/` 下。

---

## 2. 环境准备

### 前置条件

- macOS 或 Linux
- 已安装 [uv](https://github.com/astral-sh/uv)（Python 包管理器）

### 安装依赖

```bash
uv sync
```

这会根据 `pyproject.toml` 安装 Sphinx、Furo、MyST-Parser 等所有依赖到 `.venv/`。

---

## 3. 常用命令

### 全站构建

| 任务 | 命令 |
|---|---|
| 构建全部 4 个站点 | `make html` |
| 构建并启动本地预览 | `make serve`（访问 http://localhost:8000） |
| 清理构建产物 | `make clean` |

### 单产品构建

进入产品目录后使用产品级 Makefile：

```bash
# MatrixOne
cd matrixone && make html        # 中文 + 英文
cd matrixone && make html-zh     # 只构建中文
cd matrixone && make html-en     # 只构建英文

# MatrixOne Intelligence（同形）
cd matrixone-intelligence && make html
cd matrixone-intelligence && make html-zh
cd matrixone-intelligence && make html-en
```

> 提示：开发单篇文章时，建议只构建对应产品的对应语言，速度更快。

### 构建产物

```
build/html/
├── index.html                              # 产品选择页
├── matrixone/
│   ├── index.html                          # 自动按浏览器语言跳转 zh/ 或 en/
│   ├── zh/                                 # MatrixOne 中文站
│   └── en/                                 # MatrixOne 英文站
└── matrixone-intelligence/
    ├── index.html                          # 同上自动跳转
    ├── zh/                                 # Intelligence 中文站
    └── en/                                 # Intelligence 英文站
```

---

## 4. 目录结构说明

```
项目根目录/
├── Makefile                               # 根入口：委派给各产品 + 生成产品选择页和跳转页
├── pyproject.toml                         # uv 依赖声明
│
├── matrixone/                             # MatrixOne 产品
│   ├── conf.py                            # Sphinx 主配置（中英共用，通过 SPHINX_LANG 环境变量切换）
│   ├── Makefile                           # html / html-zh / html-en
│   └── source/
│       ├── _static/                       # 全局共享的主题资源（CSS / JS / 图片）
│       │   ├── css/custom.css             # 品牌化样式（:root 集中色值）
│       │   └── js/                        # topbar / breadcrumb / lang-switcher 等
│       ├── _templates/                    # Jinja 模板覆盖（预留）
│       ├── zh/                            # 中文内容
│       │   ├── index.md                   # 中文首页
│       │   ├── getting-started/           # 章节目录
│       │   │   ├── index.md               # 章节索引（含 toctree）
│       │   │   └── quickstart.md          # 具体文章
│       │   └── ...
│       └── en/                            # 英文内容（目录结构与 zh/ 镜像）
│           ├── index.md
│           └── ...
│
├── matrixone-intelligence/                # MatrixOne Intelligence 产品（同形）
│   ├── conf.py                            # 继承 matrixone/conf.py，覆盖品牌字段
│   ├── Makefile
│   └── source/
│       ├── _static -> ../../matrixone/source/_static      # symlink，共享主题
│       ├── _templates -> ../../matrixone/source/_templates # symlink
│       ├── zh/                            # 中文内容（479 篇）
│       │   ├── index.md                   # 中文首页
│       │   ├── start.md                   # 章节索引（"快速开始"）
│       │   ├── genai-workspace.md         # 章节索引（"GenAI 工作区"）
│       │   └── Get-Started/
│       │       └── quickstart.md
│       └── en/                            # 英文内容（5 篇核心文档）
│           ├── index.md
│           └── ...
│
└── scripts/
    ├── build_picker.py                    # 生成根目录产品选择页
    ├── migrate_from_mkdocs.py             # MatrixOne 迁移脚本
    └── migrate_intelligence.py            # Intelligence 迁移脚本
```

### 关键设计

- **产品隔离**：每个产品是独立子项目，有自己的 `conf.py` 和 `Makefile`，可以单独构建。
- **配置继承**：`matrixone-intelligence/conf.py` 通过 `from conf import *` 继承 `matrixone/conf.py`，只覆盖品牌字段。修改主题只需改 matrixone 一处。
- **中英共用 conf.py**：同一个产品的中英文共用一个 `conf.py`，通过 `SPHINX_LANG` 环境变量切换 `language` 和品牌标题，Makefile 在调用时自动设置。
- **静态资源共享**：`matrixone-intelligence/source/_static` 是指向 `matrixone/source/_static` 的 symlink，CSS/JS/图片全局统一，只维护一份。
- **toctree 两层结构**（Intelligence 中文站）：主索引 `index.md` → 章节索引（如 `start.md`、`genai-workspace.md`）→ 具体文章。

---

## 5. 添加新文章

### 5.1 在已有章节中添加

以在 Intelligence 中文站的「快速开始」章节下添加一篇 `my-guide.md` 为例：

**第一步：创建文件**

在 `matrixone-intelligence/source/zh/Get-Started/` 下新建 `my-guide.md`：

```markdown
# 我的新指南

这是文章正文。

## 第一节

内容...

## 第二节

内容...
```

**第二步：挂进 toctree**

编辑章节索引文件 `matrixone-intelligence/source/zh/start.md`，在对应的 toctree 块中添加路径（不带 `.md` 后缀）：

```markdown
```{toctree}
:maxdepth: 2
:caption: 概述

Get-Started/workspace
Get-Started/quickstart
Get-Started/vector
Get-Started/my-guide
```　
```

**第三步：构建预览**

```bash
cd matrixone-intelligence && make html-zh
```

然后用浏览器打开 `build/html/matrixone-intelligence/zh/Get-Started/my-guide.html` 查看效果。

### 5.2 添加全新章节

以在 Intelligence 中文站添加一个「安全管理」章节为例：

**第一步：创建目录和文章**

```
matrixone-intelligence/source/zh/
└── Security/
    ├── access-control.md
    └── audit-log.md
```

**第二步：创建章节索引**

在 `matrixone-intelligence/source/zh/` 下新建 `security.md`：

```markdown
# 安全管理

```{toctree}
:maxdepth: 2

Security/access-control
Security/audit-log
```　
```

**第三步：挂进主索引**

编辑 `matrixone-intelligence/source/zh/index.md`，在底部的 toctree 中添加一行：

```markdown
```{toctree}
:caption: MatrixOne Intelligence
:maxdepth: 1
:hidden:

主页 <self>
关于 MatrixOne Intelligence <intro>
快速开始 <start>
GenAI 工作区 <genai-workspace>
数据库实例 <db-instance>
安全管理 <security>
...
```　
```

**第四步：构建预览**

```bash
cd matrixone-intelligence && make html-zh
```

---

## 6. Markdown 写作规范

本项目使用 MyST-Parser，兼容标准 Markdown，同时支持以下扩展语法。

### 6.1 标题

每篇文章以一个 `#` 一级标题开头，作为页面标题。正文中使用 `##`、`###`、`####` 组织层级。

```markdown
# 页面标题

## 二级标题

### 三级标题
```

### 6.2 提示框（Admonition）

使用 MyST 的 colon fence 语法：

```markdown
:::{note}
这是一条提示信息。
:::

:::{warning}
这是一条警告信息。
:::

:::{tip}
这是一条建议。
:::
```

支持的类型：`note`、`warning`、`tip`、`important`、`caution`、`danger`、`hint`、`seealso`。

### 6.3 代码块

标准 Markdown 代码块，支持语言高亮和复制按钮（由 sphinx-copybutton 自动添加）：

````markdown
```sql
SELECT * FROM my_table WHERE id = 1;
```

```python
import pymysql
conn = pymysql.connect(host='localhost', user='root')
```

```bash
mysql -h 127.0.0.1 -P 6001 -u root -p
```
````

### 6.4 表格

标准 Markdown 表格：

```markdown
| 参数 | 类型 | 说明 |
|---|---|---|
| host | string | 数据库地址 |
| port | int | 端口号，默认 6001 |
```

### 6.5 链接

**站内链接**（推荐用相对路径，不带 `.md` 后缀）：

```markdown
详见 [快速开始](Get-Started/quickstart)。
```

**外部链接**：

```markdown
访问 [MatrixOne 官网](https://matrixorigin.cn)。
```

### 6.6 图片

项目中的图片大多使用 CDN 地址，直接引用即可：

```markdown
![架构图](https://community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/arch.png)
```

如需使用本地图片，放在文章同级的 `images/` 目录下：

```markdown
![示意图](./images/my-diagram.png)
```

### 6.7 sphinx-design 组件

**卡片网格**（常用于首页入口）：

```markdown
::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} 卡片标题
:link: path/to/page
:link-type: doc

卡片描述文字。
:::

::::
```

**Tab 切换**：

```markdown
::::{tab-set}

:::{tab-item} Linux
Linux 下的操作步骤...
:::

:::{tab-item} macOS
macOS 下的操作步骤...
:::

::::
```

**折叠块**：

```markdown
:::{dropdown} 点击展开详情
这里是折叠的内容。
:::
```

---

## 7. 中英文协作指南

### 7.1 整体架构

每个产品的中英文内容放在同一个 `source/` 目录下，按语言分子目录：

```
matrixone-intelligence/
├── conf.py                    ← 中英共用，SPHINX_LANG 切换品牌标题
├── Makefile                   ← html-zh / html-en 分别构建
└── source/
    ├── _static -> ...         ← symlink，共享主题
    ├── zh/                    ← 中文内容（完整）
    │   ├── index.md
    │   ├── start.md           ← 章节索引
    │   └── Get-Started/
    │       └── quickstart.md
    └── en/                    ← 英文内容（部分翻译）
        ├── index.md           ← 精简 toctree，只挂已翻译的页面
        └── Get-Started/
            └── quickstart.md  ← 与中文同路径
```

关键点：
- 中英文的**文件相对路径必须一一对应**（如 `Get-Started/quickstart.md`），语言切换按钮靠路径匹配来跳转
- 英文站的 toctree **只挂已翻译的页面**，不需要和中文站完全一致
- 两个语言共用一个 `conf.py`，通过 `SPHINX_LANG` 环境变量区分

### 7.2 同步修改中英文的完整流程

以修改 Intelligence 的 `quickstart` 文章为例：

**第一步：修改中文**

编辑 `matrixone-intelligence/source/zh/Get-Started/quickstart.md`，完成内容变更。

**第二步：同步修改英文**

编辑 `matrixone-intelligence/source/en/Get-Started/quickstart.md`，翻译对应的变更。

两个文件的结构（标题层级、章节顺序）应保持一致，方便读者在中英文之间切换时找到对应内容。

**第三步：分别构建验证**

```bash
cd matrixone-intelligence
make html-zh    # 构建中文
make html-en    # 构建英文
```

分别打开两个页面确认渲染正确。

### 7.3 新增一篇文章并同时提供英文版

以在「快速开始」章节下新增 `my-guide.md` 为例：

**第一步：创建中文文章**

新建 `matrixone-intelligence/source/zh/Get-Started/my-guide.md`，写好中文内容。

**第二步：挂进中文 toctree**

编辑 `matrixone-intelligence/source/zh/start.md`：

```markdown
```{toctree}
:maxdepth: 2
:caption: 概述

Get-Started/workspace
Get-Started/quickstart
Get-Started/vector
Get-Started/my-guide
```　
```

**第三步：创建英文文章**

新建 `matrixone-intelligence/source/en/Get-Started/my-guide.md`，路径必须和中文一致。

**第四步：挂进英文 toctree**

英文站目前页面较少，所有页面直接挂在 `matrixone-intelligence/source/en/index.md` 的 toctree 里：

```markdown
```{toctree}
:caption: MatrixOne Intelligence
:maxdepth: 1
:hidden:

Home <self>
5-Minute Quickstart <Get-Started/quickstart>
My New Guide <Get-Started/my-guide>
Core Concepts <Overview/matrixone-intelligence-introduction>
API Reference <workflow-api/automic_api>
FAQ <FAQs/FAQ-Product>
```　
```

**第五步：注册语言切换白名单**

编辑 `matrixone/source/_static/js/lang-switcher.js`，在 `PARTIAL_EN['matrixone-intelligence']` 数组中添加新页面的 HTML 路径：

```javascript
var PARTIAL_EN = {
  'matrixone-intelligence': [
    '', 'index.html',
    'Get-Started/quickstart.html',
    'Get-Started/my-guide.html',        // ← 新增
    'Overview/matrixone-intelligence-introduction.html',
    'workflow-api/automic_api.html',
    'FAQs/FAQ-Product.html'
  ]
};
```

不加这一步的话，中文页面上不会出现切换到英文的按钮。

**第六步：构建全站验证**

```bash
cd matrixone-intelligence && make html
```

然后在浏览器中测试语言切换是否正常。

### 7.4 语言切换按钮的工作原理

`lang-switcher.js` 通过 URL 路径来判断当前语言和产品：

```
/matrixone-intelligence/zh/Get-Started/quickstart.html
 ──────────┬──────────  ┬  ──────────┬──────────────
         product       lang         rest
```

切换时，只替换 `lang` 部分（`zh` ↔ `en`），`product` 和 `rest` 保持不变。所以中英文文件的**相对路径必须完全一致**。

按钮的显示逻辑由两个常量控制：

| 场景 | 按钮行为 |
|---|---|
| 产品在 `HAS_EN` 中（如 `matrixone`） | 所有页面都显示中英切换 |
| 产品在 `PARTIAL_EN` 中，当前页在白名单里 | 显示切换按钮 |
| 产品在 `PARTIAL_EN` 中，当前页不在白名单里 | 中文页不显示 "EN" 按钮（避免 404） |
| 英文页 → 中文 | 始终显示（中文站是全集） |
| 某产品英文翻译全部完成 | 从 `PARTIAL_EN` 移除，加到 `HAS_EN` |

### 7.5 中英文 toctree 结构差异

中文站和英文站的 toctree 不需要完全一致。当前项目的实际做法：

| | 中文站 | 英文站 |
|---|---|---|
| Intelligence 首页 toctree | 挂 13 个章节索引 | 只挂 4 篇已翻译的文章 |
| 章节索引文件 | 有（`start.md`、`genai-workspace.md` 等） | 没有（文章太少，直接挂在首页） |
| 导航深度 | 两层（首页 → 章节索引 → 文章） | 一层（首页 → 文章） |

随着英文翻译覆盖率提高，可以逐步给英文站也加上章节索引文件。

### 7.6 只改中文不改英文

如果某次修改只涉及中文（比如修正一个中文表述），不需要动英文站的任何文件。中英文是独立构建的，互不影响。

但如果修改涉及**结构变更**（比如重命名文件、调整目录），且该文件有英文版，则需要同步调整英文站的文件路径和 toctree，否则语言切换会跳到 404。

### 7.7 检查清单

每次涉及中英文同步修改时，对照这个清单：

- [ ] 中文文件已修改/创建（`source/zh/` 下）
- [ ] 英文文件已修改/创建（`source/en/` 下，路径与中文一致）
- [ ] 中文 toctree 已更新
- [ ] 英文 toctree 已更新
- [ ] `lang-switcher.js` 的 `PARTIAL_EN` 已更新（仅部分翻译的产品需要）
- [ ] 构建通过（`make html`）
- [ ] 浏览器中测试语言切换按钮正常工作

---

## 8. 添加新产品

如果需要添加第三个产品（如 `matrixflow`）：

### 第一步：创建目录结构

```
matrixflow/
├── conf.py
├── Makefile
└── source/
    ├── _static -> ../../matrixone/source/_static      # symlink
    ├── _templates -> ../../matrixone/source/_templates # symlink
    ├── zh/
    │   └── index.md
    └── en/
        └── index.md
```

### 第二步：编写 conf.py

```python
"""MatrixFlow 文档"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "matrixone"))

from conf import *  # noqa: F401, F403, E402

_lang = os.environ.get("SPHINX_LANG", "zh_CN")

project = "MatrixFlow Docs" if _lang == "en" else "MatrixFlow 文档"
html_title = project
copyright = "2026, MatrixOne"
```

### 第三步：编写 Makefile

```makefile
.PHONY: html html-zh html-en clean

BUILD = ../build/html/matrixflow

html-zh:
	SPHINX_LANG=zh_CN uv run sphinx-build -a -c . -D language=zh_CN -b html source/zh $(BUILD)/zh

html-en:
	SPHINX_LANG=en uv run sphinx-build -a -c . -D language=en -b html source/en $(BUILD)/en

html: html-zh html-en

clean:
	rm -rf $(BUILD)
```

### 第四步：创建 symlink

```bash
ln -s ../../matrixone/source/_static matrixflow/source/_static
ln -s ../../matrixone/source/_templates matrixflow/source/_templates
```

### 第五步：更新根 Makefile

在根 `Makefile` 中添加：

```makefile
matrixflow:
	$(MAKE) -C matrixflow html
```

并在 `html:` 目标的依赖列表和 `redirects:` 段中添加对应条目。

### 第六步：更新产品选择页

编辑 `scripts/build_picker.py`，在 HTML 模板的 `.cards` 区域添加一张新的产品卡片。

---

## 9. 主题与样式定制

### 样式文件

所有自定义样式集中在 `matrixone/source/_static/css/custom.css`，修改后所有产品自动生效（通过 symlink 共享）。

CSS 文件顶部的 `:root` 区域定义了设计 Token（颜色变量），修改品牌色只需调整这些变量。

### JS 功能模块

| 文件 | 功能 |
|---|---|
| `topbar.js` | 顶部导航栏（logo、搜索框、导航 tab） |
| `breadcrumb.js` | 面包屑导航 |
| `lang-switcher.js` | 中英文切换按钮 |
| `version-switcher.js` | 版本切换器（当前为 UI 占位） |
| `mo-highlight.js` | MatrixOne 方言关键字高亮（SNAPSHOT、CLONE 等） |
| `feedback.js` | 页面底部反馈组件 |
| `footer.js` | 自定义页脚 |
| `assistant.js` | 右下角文档助手浮窗（占位，需接 RAG 后端） |
| `icons.js` | Intelligence 首页卡片 SVG 图标注入 |

所有 JS 文件位于 `matrixone/source/_static/js/`，其他产品通过 symlink 共享。

### Furo 主题配置

在 `matrixone/conf.py` 的 `html_theme_options` 中配置：

```python
html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#004af0",    # 品牌主色
        "color-brand-content": "#004af0",    # 内容区链接色
    },
    "dark_css_variables": {
        "color-brand-primary": "#6b8cff",
        "color-brand-content": "#6b8cff",
    },
}
```

---

## 10. 注意事项

1. **文件必须被 toctree 引用**：未被任何 toctree 引用的 `.md` 文件不会出现在导航中，Sphinx 会输出 warning。
2. **toctree 路径不带 `.md` 后缀**：这是 Sphinx/MyST 的约定。
3. **不要复制 `_static` 和 `_templates` 目录**：始终使用 symlink 指向 `matrixone/source/_static/` 和 `matrixone/source/_templates/`，确保样式统一且只维护一份。
4. **conf.py 用继承不用复制**：通过 `from conf import *` 继承主配置，避免配置漂移。
5. **图片优先用 CDN**：本项目的图片大多托管在腾讯云 COS CDN 上，新增图片建议也上传到 CDN 后引用 URL。
6. **构建 warning 已静默**：`conf.py` 中配置了 `suppress_warnings` 来忽略跨章节断链警告（因为部分内容是迁移过来的）。全量校验时应移除此配置，逐个修复断链。
7. **目录名避免空格**：Sphinx 生成的 URL 会把空格编码为 `%20`，影响可读性和兼容性。
8. **中英文路径必须一致**：语言切换按钮通过替换 URL 中的 `zh`/`en` 来跳转，如果中英文文件路径不一致会导致 404。
9. **单产品构建要进子目录**：`cd matrixone && make html-zh`，不要在根目录直接跑产品级命令。

---

## 11. 故障排查

| 问题 | 原因 | 解决方案 |
|---|---|---|
| 构建报 `myst.xref_missing` | 文章中引用了不存在的页面 | 已被 `suppress_warnings` 静默；如需修复，检查链接目标是否存在 |
| 新文章不出现在导航中 | 未在 toctree 中添加路径 | 编辑对应的章节索引文件，添加文件路径 |
| 样式/JS 不生效 | `_static` symlink 断了 | 重新创建：`ln -s ../../matrixone/source/_static source/_static` |
| 构建后页面空白 | `.md` 文件缺少一级标题 | 确保每篇文章以 `# 标题` 开头 |
| 语言切换按钮不显示 | 页面不在 `PARTIAL_EN` 白名单中 | 编辑 `lang-switcher.js`，将页面路径加入白名单 |
| `make serve` 端口被占用 | 8000 端口已有进程 | 先停掉占用进程，或手动指定端口 |
| 构建时品牌标题不对 | `SPHINX_LANG` 环境变量未设置 | 使用产品 Makefile 的 `html-zh` / `html-en` 目标，它会自动设置 |
| Intelligence 构建找不到主题 | conf.py 的 `sys.path.insert` 路径不对 | 确认 `matrixone/conf.py` 存在且路径正确 |
