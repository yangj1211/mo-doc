# 使用指南

本文档面向内容作者和开发者，介绍如何在本项目中添加、编辑和构建文档。

---

## 1. 项目简介

这是一个基于 **Sphinx + MyST + Furo** 的多产品文档站，支持中英双语，目前包含两个产品：

| 产品 | 中文源目录 | 英文源目录 | 构建产物路径 |
|---|---|---|---|
| MatrixOne（数据库） | `source/` | `source_en/` | `build/html/matrixone/{zh,en}/` |
| MatrixOne Intelligence（AI 平台） | `intelligence/` | `intelligence_en/` | `build/html/intelligence/{zh,en}/` |

内容全部用 **Markdown** 编写（通过 MyST-Parser 解析），支持 `sphinx-design` 的卡片/网格/Tab 组件和 `sphinx-copybutton` 的代码复制按钮。

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

| 任务 | 命令 |
|---|---|
| 构建全部 4 个站点 | `make html` |
| 构建并启动本地预览 | `make serve`（访问 http://localhost:8000） |
| 清理构建产物 | `make clean` |
| 仅构建 MatrixOne 中文 | `uv run sphinx-build -a -b html source build/html/matrixone/zh` |
| 仅构建 MatrixOne 英文 | `uv run sphinx-build -a -b html source_en build/html/matrixone/en` |
| 仅构建 Intelligence 中文 | `uv run sphinx-build -a -b html intelligence build/html/intelligence/zh` |
| 仅构建 Intelligence 英文 | `uv run sphinx-build -a -b html intelligence_en build/html/intelligence/en` |

> 提示：开发单篇文章时，建议只构建对应的子站，速度更快。

---

## 4. 目录结构说明

```
项目根目录/
├── source/                    # MatrixOne 中文（主站点，主题资源在这里）
│   ├── conf.py                # Sphinx 主配置（所有子站继承此文件）
│   ├── index.md               # 中文首页
│   ├── _static/
│   │   ├── css/custom.css     # 全局自定义样式
│   │   ├── js/                # topbar / breadcrumb / lang-switcher 等 JS
│   │   └── images/            # logo 等静态图片
│   └── getting-started/       # 内容目录（按章节组织）
│       ├── index.md           # 章节索引（含 toctree）
│       └── quickstart.md      # 具体文章
│
├── source_en/                 # MatrixOne 英文
│   ├── conf.py                # 继承 source/conf.py，覆盖 language / html_title
│   ├── _static -> ../source/_static   # symlink，共享样式和 JS
│   └── ...                    # 目录结构与 source/ 一一对应
│
├── intelligence/              # Intelligence 中文
│   ├── conf.py                # 继承 source/conf.py，覆盖产品名
│   ├── _static -> ../source/_static   # symlink
│   ├── index.md               # 中文首页
│   ├── start.md               # 章节索引（"快速开始"）
│   ├── genai-workspace.md     # 章节索引（"GenAI 工作区"）
│   └── Get-Started/           # 内容目录
│       └── quickstart.md
│
├── intelligence_en/           # Intelligence 英文（目前仅 5 篇核心文档）
│   ├── conf.py                # 继承 source/conf.py，覆盖产品名 + language
│   ├── _static -> ../source/_static
│   └── ...
│
├── scripts/
│   ├── build_picker.py        # 生成根目录产品选择页
│   ├── migrate_from_mkdocs.py # MatrixOne 迁移脚本
│   └── migrate_intelligence.py# Intelligence 迁移脚本
│
├── Makefile                   # 构建入口
└── build/html/                # 构建产物（git 忽略）
```

### 关键设计

- **配置继承**：所有子站的 `conf.py` 通过 `from conf import *` 继承 `source/conf.py`，只覆盖产品名、标题等字段。修改主题只需改一处。
- **静态资源共享**：`source_en/`、`intelligence/`、`intelligence_en/` 的 `_static` 都是指向 `source/_static/` 的 symlink，CSS/JS/图片全局统一。
- **toctree 两层结构**：主索引 `index.md` → 章节索引（如 `start.md`）→ 具体文章。

---

## 5. 添加新文章

### 5.1 在已有章节中添加

以在 Intelligence 中文站的「快速开始」章节下添加一篇 `my-guide.md` 为例：

**第一步：创建文件**

在 `intelligence/Get-Started/` 下新建 `my-guide.md`：

```markdown
# 我的新指南

这是文章正文。

## 第一节

内容...

## 第二节

内容...
```

**第二步：挂进 toctree**

编辑章节索引文件 `intelligence/start.md`，在对应的 toctree 块中添加路径（不带 `.md` 后缀）：

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
uv run sphinx-build -a -b html intelligence build/html/intelligence/zh
```

然后用浏览器打开 `build/html/intelligence/zh/Get-Started/my-guide.html` 查看效果。

### 5.2 添加全新章节

以添加一个「安全管理」章节为例：

**第一步：创建目录和文章**

```
intelligence/
└── Security/
    ├── access-control.md
    └── audit-log.md
```

**第二步：创建章节索引**

在 `intelligence/` 下新建 `security.md`：

```markdown
# 安全管理

```{toctree}
:maxdepth: 2

Security/access-control
Security/audit-log
```　
```

**第三步：挂进主索引**

编辑 `intelligence/index.md`，在底部的 toctree 中添加一行：

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
make html
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

中文和英文是**两套独立的 Sphinx 站点**，各自有自己的源目录、`conf.py` 和 toctree 结构：

```
intelligence/              ← 中文站（完整，约 480 篇）
├── conf.py
├── index.md               ← 中文首页 + 完整 toctree
├── start.md               ← 章节索引（引用 6 篇文章）
├── genai-workspace.md     ← 章节索引（引用 20+ 篇文章）
└── Get-Started/
    └── quickstart.md

intelligence_en/           ← 英文站（部分翻译，目前 5 篇）
├── conf.py
├── index.md               ← 英文首页 + 精简 toctree（只挂已翻译的页面）
├── Get-Started/
│   └── quickstart.md      ← 与中文同路径
└── ...
```

关键点：
- 中英文的**文件路径必须一一对应**（如 `Get-Started/quickstart.md`），语言切换按钮靠路径匹配来跳转
- 英文站的 toctree **只挂已翻译的页面**，不需要和中文站完全一致
- 两个站共享同一套 `_static`（CSS/JS），通过 symlink 实现

### 7.2 同步修改中英文的完整流程

以修改 Intelligence 的 `quickstart` 文章为例，假设你需要同时更新中英文内容：

**第一步：修改中文**

编辑 `intelligence/Get-Started/quickstart.md`，完成内容变更。

**第二步：同步修改英文**

编辑 `intelligence_en/Get-Started/quickstart.md`，翻译对应的变更。

两个文件的结构（标题层级、章节顺序）应保持一致，方便读者在中英文之间切换时找到对应内容。

**第三步：分别构建验证**

```bash
# 构建中文
uv run sphinx-build -a -b html intelligence build/html/intelligence/zh

# 构建英文
uv run sphinx-build -a -b html intelligence_en build/html/intelligence/en
```

分别打开两个页面确认渲染正确。

### 7.3 新增一篇文章并同时提供英文版

以在「快速开始」章节下新增 `my-guide.md` 为例：

**第一步：创建中文文章**

新建 `intelligence/Get-Started/my-guide.md`，写好中文内容。

**第二步：挂进中文 toctree**

编辑 `intelligence/start.md`：

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

新建 `intelligence_en/Get-Started/my-guide.md`，路径必须和中文一致。

**第四步：挂进英文 toctree**

英文站没有 `start.md` 这样的章节索引（因为只有少量页面），所有页面直接挂在 `intelligence_en/index.md` 的 toctree 里：

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

编辑 `source/_static/js/lang-switcher.js`，在 `PARTIAL_EN.intelligence` 数组中添加新页面的 HTML 路径：

```javascript
var PARTIAL_EN = {
  intelligence: [
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
make html
```

然后在浏览器中测试：
- 打开中文页 `build/html/intelligence/zh/Get-Started/my-guide.html`，确认右上角出现 "EN" 切换按钮
- 点击切换到英文页，确认内容正确

### 7.4 语言切换按钮的工作原理

`lang-switcher.js` 通过 URL 路径来判断当前语言和产品：

```
/intelligence/zh/Get-Started/quickstart.html
 ─────┬─────  ┬  ──────────┬──────────────
    product  lang         rest
```

切换时，只替换 `lang` 部分（`zh` ↔ `en`），`product` 和 `rest` 保持不变。所以中英文文件的**相对路径必须完全一致**。

按钮的显示逻辑由两个常量控制：

```javascript
// 英文站完整覆盖中文的产品 → 所有页面都显示切换按钮
var HAS_EN = { matrixone: true };

// 英文站只翻译了部分页面的产品 → 仅白名单页面显示切换按钮
var PARTIAL_EN = {
  intelligence: [
    '', 'index.html',
    'Get-Started/quickstart.html',
    ...
  ]
};
```

| 场景 | 按钮行为 |
|---|---|
| 产品在 `HAS_EN` 中 | 所有页面都显示中英切换 |
| 产品在 `PARTIAL_EN` 中，当前页在白名单里 | 显示切换按钮 |
| 产品在 `PARTIAL_EN` 中，当前页不在白名单里 | 中文页不显示 "EN" 按钮（避免点过去 404） |
| 英文页 → 中文 | 始终显示（中文站是全集） |
| 产品既不在 `HAS_EN` 也不在 `PARTIAL_EN` | 不显示切换按钮 |

### 7.5 中英文 toctree 结构差异

中文站和英文站的 toctree 不需要完全一致。当前项目的实际做法：

| | 中文站 | 英文站 |
|---|---|---|
| 首页 toctree | 挂 13 个章节索引 | 只挂 4 篇已翻译的文章 |
| 章节索引文件 | 有（`start.md`、`genai-workspace.md` 等） | 没有（文章太少，直接挂在首页） |
| 导航深度 | 两层（首页 → 章节索引 → 文章） | 一层（首页 → 文章） |

随着英文翻译覆盖率提高，可以逐步给英文站也加上章节索引文件，让导航结构和中文站对齐。

### 7.6 MatrixOne 产品的中英文（全覆盖模式）

MatrixOne 产品的英文站已经完整覆盖中文，所以它的做法更简单：

- `source/` 和 `source_en/` 的目录结构完全镜像
- toctree 结构一一对应
- `HAS_EN` 中标记了 `matrixone: true`，所有页面自动显示切换按钮
- 不需要维护 `PARTIAL_EN` 白名单

新增文章时，在 `source/` 和 `source_en/` 下同时创建同路径文件，同时更新两边的 toctree 即可。

### 7.7 只改中文不改英文

如果某次修改只涉及中文（比如修正一个中文表述），不需要动英文站的任何文件。两个站是独立构建的，互不影响。

但如果修改涉及结构变更（比如重命名文件、调整目录），且该文件有英文版，则需要同步调整英文站的文件路径和 toctree，否则语言切换会跳到 404。

### 7.8 检查清单

每次涉及中英文同步修改时，对照这个清单：

- [ ] 中文文件已修改/创建
- [ ] 英文文件已修改/创建（路径与中文一致）
- [ ] 中文 toctree 已更新
- [ ] 英文 toctree 已更新
- [ ] `lang-switcher.js` 的 `PARTIAL_EN` 已更新（仅部分翻译的产品需要）
- [ ] `make html` 构建通过
- [ ] 浏览器中测试语言切换按钮正常工作

---

## 8. 添加新产品

如果需要添加第三个产品（如 `matrixflow`）：

### 第一步：创建目录

```
matrixflow/              # 中文
├── conf.py
├── _static -> ../source/_static    # symlink
├── index.md
└── ...

matrixflow_en/           # 英文（可选）
├── conf.py
├── _static -> ../source/_static
├── index.md
└── ...
```

### 第二步：编写 conf.py

```python
"""MatrixFlow 文档"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "source"))

from conf import *  # noqa: F401, F403, E402

project = "MatrixFlow 文档"
html_title = "MatrixFlow 文档"
copyright = "2026, MatrixOne"
```

### 第三步：创建 symlink

```bash
ln -s ../source/_static matrixflow/_static
ln -s ../source/_static matrixflow_en/_static
```

### 第四步：更新 Makefile

在 `html:` 目标中添加构建命令和跳转页：

```makefile
	uv run sphinx-build -a -b html matrixflow    $(BUILD)/matrixflow/zh
	uv run sphinx-build -a -b html matrixflow_en $(BUILD)/matrixflow/en
	@printf '%s\n' \
	  '<!doctype html>' \
	  '<meta charset="utf-8">' \
	  '<title>MatrixFlow</title>' \
	  '<script>location.replace((navigator.language||"zh").toLowerCase().indexOf("zh")===0?"zh/":"en/")</script>' \
	  '<meta http-equiv="refresh" content="0;url=zh/">' \
	  > $(BUILD)/matrixflow/index.html
```

### 第五步：更新产品选择页

编辑 `scripts/build_picker.py`，在 HTML 模板的 `.cards` 区域添加一张新的产品卡片。

---

## 9. 主题与样式定制

### 样式文件

所有自定义样式集中在 `source/_static/css/custom.css`，修改后所有子站自动生效。

CSS 文件顶部的 `:root` 区域定义了设计 Token（颜色变量），修改品牌色只需调整这些变量。

### JS 功能模块

| 文件 | 功能 |
|---|---|
| `topbar.js` | 顶部导航栏（logo、搜索框、导航 tab） |
| `breadcrumb.js` | 面包屑导航 |
| `lang-switcher.js` | 中英文切换按钮 |
| `mo-highlight.js` | MatrixOne 方言关键字高亮（SNAPSHOT、CLONE 等） |
| `feedback.js` | 页面底部反馈组件 |
| `footer.js` | 自定义页脚 |
| `assistant.js` | 右下角文档助手浮窗（占位，需接 RAG 后端） |
| `icons.js` | Intelligence 首页卡片 SVG 图标注入 |

### Furo 主题配置

在 `source/conf.py` 的 `html_theme_options` 中配置：

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
3. **不要复制 `_static` 目录**：始终使用 symlink 指向 `source/_static/`，确保样式统一且只维护一份。
4. **conf.py 用继承不用复制**：通过 `from conf import *` 继承主配置，避免配置漂移。
5. **图片优先用 CDN**：本项目的图片大多托管在腾讯云 COS CDN 上，新增图片建议也上传到 CDN 后引用 URL。
6. **构建 warning 已静默**：`conf.py` 中配置了 `suppress_warnings` 来忽略跨章节断链警告（因为 demo 只迁移了部分内容）。全量迁移后应移除此配置，逐个修复断链。
7. **目录名避免空格**：Sphinx 生成的 URL 会把空格编码为 `%20`，影响可读性和兼容性。

---

## 11. 故障排查

| 问题 | 原因 | 解决方案 |
|---|---|---|
| 构建报 `myst.xref_missing` | 文章中引用了未迁移的页面 | 已被 `suppress_warnings` 静默；如需修复，检查链接目标是否存在 |
| 新文章不出现在导航中 | 未在 toctree 中添加路径 | 编辑对应的章节索引文件，添加文件路径 |
| 样式/JS 不生效 | `_static` symlink 断了 | 重新创建：`ln -sf ../source/_static _static` |
| 构建后页面空白 | `.md` 文件缺少一级标题 | 确保每篇文章以 `# 标题` 开头 |
| 语言切换按钮不显示 | 页面不在 `PARTIAL_EN` 白名单中 | 编辑 `lang-switcher.js`，将页面路径加入白名单 |
| `make serve` 端口被占用 | 8000 端口已有进程 | 先停掉占用进程，或手动指定端口：`cd build/html && python -m http.server 9000` |
