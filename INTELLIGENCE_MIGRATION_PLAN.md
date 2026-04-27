# MatrixOne Intelligence 文档迁移分析报告

> 状态：**仅分析，未动文件**。
> 源仓库：`/Users/admin/project/moi/doc/moc-docs`（只读）
> 目标仓库：`/Users/admin/project/moi/docs-demo`
> 写于：2026-04-27

---

## 0. 先校正你描述里的几处不一致

读完两个仓库后，发现你给我的路径假设和实际文件树对不上，这会影响后面的迁移策略，先列清楚：

| 你说的 | 实际情况 |
|---|---|
| `docs-demo/matrixone/source/_static/css/` | **没有 `matrixone/` 这一层**。`source/`（中文）和 `source_en/`（英文）就在 `docs-demo/` 根目录。换句话说，**docs-demo 当前就是 matrixone 站本身**。 |
| `docs-demo/matrixone/source/_templates/` | **没有 `_templates/` 目录**。matrixone 完全靠 `_static/css/custom.css`（2284 行）+ 7 个 JS 文件 + `conf.py` 的 `html_theme_options` 实现品牌化，没有覆盖 Furo 模板。 |
| `docs-demo/MIGRATION_NOTES.md` | **不存在这个文件**。MkDocs → MyST 的迁移经验写在 `README.md` 第 163–186 行的"从 MkDocs 迁移的经验"和"关键实现备忘"两节里。下文的"已知坑"以这两节为准。 |

**这意味着加 intelligence 子站的方案有两种**（在第 4、5 节展开）：

- **A. 平铺并列**：在 docs-demo 根目录新增 `intelligence/`（zh）+ `intelligence_en/`（en），build 出 `build/html/intelligence-zh` 和 `build/html/intelligence-en`。改动小，但 `docs-demo` 根开始有 4 套 source 目录。
- **B. 重新分层**：把现有 `source/` → `matrixone/source/`、`source_en/` → `matrixone/source_en/`，新建 `intelligence/source/` 和 `intelligence/source_en/`。**符合你脑中的目录模型**，但要改 Makefile + 移文件 + 更新 README 的相对路径。

我下面默认按 **方案 A** 写（demo 阶段成本最低），方案 B 在第 5 节也给出对应步骤。

---

## 1. 源仓库技术栈识别

### 静态生成器
- **MkDocs + Material 主题**（`mkdocs-material==9.1.21`）
- 配置文件：`mkdocs.yml`（614 行，绝大部分是 nav 嵌套）
- Python 依赖（`requirements.txt`）：仅 3 个 —— `mkdocs-material`、`mike`（多版本）、`mkdocs-print-site-plugin`（PDF 风格打印站）

### 内容格式
- 纯 **Markdown**，无 MDX/MyST/rST。语法风格属于 GitHub-flavored + pymdownx 扩展。

### 主题与插件
- 主题：`material`，自定义 palette `scheme: mo`（颜色由 `docs/stylesheets/extra.css` 注入：主色 `#2035da`，浅 `#32a2ff`，深 `#1a3edb`），Ubuntu 字体
- 启用 features：`content.code.copy` / `content.action.edit` / `navigation.instant` / `navigation.tracking` / `navigation.tabs` / `navigation.tabs.sticky` / `navigation.footer`
- Plugins：`search`（自定义中文分词正则）、`print-site`、`mike`（多版本，由 `extra.version.provider: mike` 引入）

### Markdown 扩展
- `admonition`（`!!! note` 类语法）
- `pymdownx.details`（`???` 折叠块；本仓库实际**未使用**）
- `pymdownx.superfences`（fence 嵌套）
- `pymdownx.tabbed`（`alternate_style: true`，`=== "标题"` Tab）
- `def_list`（定义列表；本仓库实际**未使用**）
- `pymdownx.tasklist`（`custom_checkbox: true`，复选框）

### 自定义组件 / Shortcode
- **没有自定义组件**。没有 mermaid 块、没有 `--8<--` snippet 引用、没有 `{{ version }}` mike 宏。
- 有少量 38 个文件用了**裸 HTML**（`<font>` / `<span>` / `<div>`）做局部颜色或对齐，转 MyST 时基本可保留（MyST 默认开 `html_image` 和原生 HTML 透传）。

### 配套 lint / 工程化
- `package.json` 里挂了三套 lint：`autocorrect`（中英排版）、`zhlint`（中文标点）、`markdownlint-cli2`。
- `.autocorrectrc` 里有自定义术语字典（"MatrixOne" / "MatrixOne Intelligence" 不被改写）。
- 这些**不需要随文档迁过来**，迁移完成后由 docs-demo 自己的 markdownlint（如果有）接管即可。

---

## 2. 内容盘点

### 总文章数
- **480 篇** Markdown（其中 479 篇在 `docs/MatrixOne-Intelligence/`，1 篇是 `docs/README.md` 站点首页）

### 顶层目录结构（`docs/MatrixOne-Intelligence/`）

| 目录 | 文章数 | 大致内容 |
|---|---:|---|
| `Reference/` | **345** | SQL 参考：Operators / Functions / Variable / Data-Types / SQL-Reference / Limitations |
| `App-Develop/` | 54 | 应用开发：连接驱动（Java/Python/Go/C#）、schema 设计、事务、CRUD 教程 |
| `Charging/` | 11 | 计费 / 价格 / 充值 / 退订 |
| `workflow api/` ⚠️ | 8 | API 说明（**目录名带空格**，迁移时要改） |
| `Workspace-Mgmt/` | 7 | GenAI 工作区、用户/角色权限、数据中心 |
| `Get-Started/` | 6 | 工作区 / 实例 / 向量 / AI 搜索 / CV 搜索 / Parse 演示 —— **入口文档** |
| `Data-Processing/` | 6 | 工作流、作业、4 个工作流模板 |
| `Security/` | 5 | RBAC、TLS、IP 白名单、私网 |
| `Instance-Mgmt/` | 5 | Serverless / 标准实例创建、连接、登录、终止恢复 |
| `Migrate-Data/` | 4 | TPCH / S3 / Local / NineData 导入 |
| `Data-Explore/` | 4 | SQL Editor / Workbook / Query History / Profile |
| `Release-Notes/` | 3 | 2023 / 2024 / 2025（按年聚合，不是按版本） |
| `Protocol/` | 3 | 隐私协议 / 服务条款 / SLA |
| `Overview/` | 3 | 产品介绍 / MySQL 兼容性 |
| `Data-Connect/` | 3 | 连接器 / 数据载入 / 数据导出 |
| `Monitor/` | 2 | 监控指标 / 监控数据 |
| `FAQs/` | 2 | SQL FAQ / 产品 FAQ |
| 其他单文件 | 6 | `mcp/`、`develop/`、`Backup-Restore/`、`Data-Sharing/`、`Alarm/`、`Events/`、`tech-support.md`、`glossary.md` |

观察：**Reference 占 72%**（345/480），是典型的"SQL 大全"型参考文档；产品向 / 教程向内容只有约 130 篇，浓度集中在 Get-Started、App-Develop、Workspace-Mgmt、Data-Processing。Demo 真正能"亮出来"的，就是这 130 篇里挑代表。

### 多语言
- mkdocs.yml 里 `extra.alternate` 声明了 `/en/m1intelligence/` 和 `/zh/m1intelligence/`，配合 `mike` 实现多版本。
- **但 `docs/` 目录里只有中文**（FAQ、glossary、quickstart 全部中文标题和正文）。英文站极可能是另一条 `mike` git 分支管理，**不在当前文件树**。
- 迁移到 demo 时：**只迁中文**。要英文等正式上线，再走 demo 现有的中→英流程（matrixone 是 AI 一次翻译，README 里有说明）。

### 版本管理
- 使用 `mike` 多版本。`Dockerfile-mike` 里 `CMD ["mike", "serve", ...]`。
- 但 `docs/` 目录本身没有版本痕迹（无 `v1/` `v2/` 子目录、无 `{{ version }}` 宏）。版本由 git 分支隔离。
- **Demo 不用考虑多版本**（demo README 里也明确说多版本是 P0 待补项）。

### 图片资源（**这是最大的惊喜**）
- 仓库内 image 文件：74 个（`docs/assets/images/` + `docs/MatrixOne-Intelligence/workflow api/images/`）
- 但 markdown 里 **71 个文件**通过 CDN 引用 `community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/...`
- 全文档树里**只搜到 1 处本地相对路径图片**（`./images/api-management-entry.png`）
- **结论**：MOC 文档站的图片几乎全走腾讯云 CDN，迁过来直接保留 URL 即可，**不会有断图风险，也不需要 image path remapping**。这点比 matrixone 的"图片必须 cp -R 保持相对路径"简单得多。

### 内容分类（按文档站典型分桶）
| 类型 | 在 moc-docs 中的位置 |
|---|---|
| 快速开始 | `Get-Started/` 6 篇（workspace / quickstart / vector / ai_search / cv_search / parse_demo） |
| 概念 / 概述 | `Overview/`、`Workspace-Mgmt/overview.md`、`glossary.md` |
| 教程 | `App-Develop/Tutorial/` 9 篇（Java / Python / Go / C# / SpringBoot / SQLAlchemy / Django / Gorm） |
| API 参考 | `workflow api/` 8 篇 |
| SQL 参考 | `Reference/` 345 篇 |
| FAQ | `FAQs/` 2 篇 |
| Release Notes | `Release-Notes/` 3 篇 |
| 法务 | `Protocol/` 3 篇 |

---

## 3. 迁到 Sphinx + MyST 的难度评估

对照 docs-demo `README.md` 第 163–186 行（matrixone 自己的迁移经验）和 `conf.py` 的 `myst_enable_extensions`：

### 已知坑（matrixone 迁移时已经踩过、有现成解法）

| 坑 | moc-docs 命中情况 | 处理方案 |
|---|---|---|
| `!!! note` admonition → `:::{note}` | **74 处**，分散在 ~38 个文件 | 一行 sed 或 5 行 Python regex 批量转换 |
| `=== "tab"` Tab 容器 → `{tab-set}` + `{tab-item}` | **2 个文件**（都是 `App-Develop/export-data/modump.md`，4 处 tab 标签） | 手工改 5 分钟，或写个简单的 Python 转换器 |
| `??? collapsible` 折叠块 → `:::{dropdown}` | **0 处** | 不需要处理 |
| 跨目录链接大小写漂移 | 待批量扫，但 moc-docs 目录大小写规范度比 matrixone 老仓库**好得多**（无明显 `Overview/` vs `overview/` 混用） | 估计 0–少量 case，到时 sed 即可 |
| 老 RN 里 `***` 紧跟标题 docutils 报错 | 待全量 build 时才能确认 | 单点 sed |
| 未迁目录 broken link | 一定会有（精选迁移时尤其多） | conf.py 里 `suppress_warnings = ["myst.xref_missing"]`（demo 已开） |

### 新坑（matrixone 没遇到，moc-docs 有）

| 坑 | 严重度 | 处理方案 |
|---|---|---|
| **目录名带空格**：`workflow api/`（8 篇 + 一个 `images/` 子目录） | 中 | 迁移时改名 `workflow-api/`，并在转换脚本里把所有 `(workflow%20api/...)` 和 `(workflow api/...)` 链接同步改名。否则 Sphinx 生成的 URL 会带 `%20` 很丑，且部分浏览器 / CDN 会出问题 |
| **Reference/Operators/operators/operators/** 三层重名嵌套 | 低 | 不破坏功能，但 toctree 看起来奇怪。**不修**（精选迁移时不会迁这块），全量迁移时建议拍平 |
| `pymdownx.details`、`def_list`、`pymdownx.tasklist` 扩展声明了但**实际没用** | 低 | 直接忽略，conf.py 不用加对应 myst 扩展 |
| 38 个文件含**裸 HTML**（`<font color>` / `<span>` / `<div align>`） | 低 | MyST 默认透传 HTML，绝大多数能直接渲染。`<font>` 是过时标签但浏览器仍解析。要严谨可在迁移脚本里替换为 `:::{div}` + class，但**demo 阶段不必** |
| Material 主题特有的 `content.action.edit` / `navigation.tabs.sticky` / `print-site` 插件 | 低 | Furo 没有"页面顶部 tab 导航"对等物（用左侧 toctree 替代）；编辑链接 Furo 有 `source_repository` 配置；print-site 没有对等物，demo 阶段不需要 |
| 站点首页 `docs/README.md` 用了 `**加粗标题**` 这种 Material 风格 | 极低 | matrixone 的 `index.md` 已经示范了 hero + grid 卡片的写法，照抄即可 |
| Mike 的版本切换 UI | 不影响 demo | demo 已明确不做多版本 |

### 总体难度判断
- moc-docs 的 Markdown 健康度**比 matrixone 当年好**（只用了 `admonition` + 极少 `tabbed` + 0 mermaid + 0 snippet + 0 mike 宏 + 图片走 CDN 不需要路径重映射）。
- matrixone 当年迁 630 篇估算 2–3 天，moc-docs 要全量迁 **480 篇**，按相同方法 **1.5–2 天**就能搬完（含批量转换脚本 + 抽样修 broken link）。

---

## 4. 推荐迁移策略

### 策略 A：全量迁移
- **做什么**：480 篇全部转过来，沿用 matrixone 的 `source/` + `source_en/` 模式，结果是 demo 出现 4 套 source 目录或一个新 `intelligence/` 子目录
- **工作量**：1.5–2 天（写脚本 4h + 跑批 + 抽检 + 修 broken link 1d）
- **适用**：moc-docs 已经是产品官方文档，内容稳定，全量搬过来是终态
- **不适合 demo 阶段的理由**：
  - Reference 345 篇是 SQL 函数 / 操作符的参考墙，研发看 demo 不会一篇篇点开；演示价值低
  - 全量迁完需要校验近 500 篇，**任何一篇 broken link 都拉低 demo 可信度**，不如 4–6 篇做精

### 策略 B：精选迁移（**推荐**）⭐
- **做什么**：只迁 5 篇代表性文章，其他靠 toctree 占位 + `:::{tip} 完整内容请看 ...` 跳转回 moc-docs 官网
- **挑哪 5 篇**（已根据上面盘点核对存在性）：

  | 文档类型 | moc-docs 源文件 | demo 目标位置 |
  |---|---|---|
  | 快速开始 | `MatrixOne-Intelligence/Get-Started/quickstart.md` (70 行) | `intelligence/getting-started/quickstart.md` |
  | 核心概念 | `MatrixOne-Intelligence/Workspace-Mgmt/overview.md` | `intelligence/concepts/workspace.md` |
  | 教程 | `MatrixOne-Intelligence/Get-Started/vector.md`（向量能力，AI 数据库的招牌特性） | `intelligence/tutorials/vector.md` |
  | API 参考 | `MatrixOne-Intelligence/workflow api/automic_api.md` (756 行，有完整的 Tab + admonition 用例) | `intelligence/api/atomic-api.md` |
  | FAQ | `MatrixOne-Intelligence/FAQs/FAQ-Product.md` (45 行) | `intelligence/faq/product.md` |

- **工作量估算**：
  - 拷文件 + 路径改名：30 分钟
  - 跑 sed 转换 `!!! note` → `:::{note}`、`=== "x"` → `{tab-set}`：30 分钟
  - 写 `intelligence/conf.py`（继承 / 复用 matrixone 主题）：30 分钟
  - 写 `intelligence/index.md`（仿 matrixone 的 hero + 6 张入口卡）：1h
  - Makefile 加一条 build target：15 分钟
  - 本地 `make html` 验证 + 修 broken link：1h
  - **总计：3.5–4h**，半个工作日搞定

- **适用**：你的明确目标 —— "让研发看到 intelligence 文档站的样子，不要求内容完整"。和 matrixone 之前迁 61 篇做 demo 的思路完全一致。

### 策略 C：全部新写
- **做什么**：不迁旧内容，照 matrixone 的 4 篇样本（`quickstart.md` / `data-branch.md` / `snapshot.md` / `faq.md`）的骨架，纯手写 4 篇 intelligence 占位文（每篇 500–1500 字）
- **工作量**：4 篇 × 1.5h = 6h（写作时间最不可控）
- **适用**：moc-docs 内容质量差或风格 matrixone 完全不兼容
- **不推荐的理由**：moc-docs 已有 480 篇产品文档，质量并不差（FAQ / quickstart 都是完整可用的中文段落），**舍弃可用素材去手写是浪费**。除非你想让 intelligence demo 用一套和真实产品完全脱钩的虚构内容，这没必要。

### 推荐
**策略 B**。理由：
1. demo 的目的就是让研发"看见"，不是"读完"，5 篇覆盖 5 种类型已经够展示信息架构 + 排版风格
2. moc-docs 内容现成可用，挑 5 篇成本低于手写 4 篇
3. 万一 demo 通过、需要全量上线，已经验证过转换链路，再走策略 A 只是"重复同一动作 96 次"

---

## 5. 风格一致性方案（intelligence 复用 matrixone 主题）

> 校正：实际 docs-demo 没有 `_templates/`，主题完全靠 `_static/css/custom.css` + `_static/js/*.js` + `conf.py` 实现。

### 方案 A（平铺并列，推荐 demo 用这个）

新文件 / 目录：
```
docs-demo/
├── source/                 # 既有 matrixone 中文，不动
├── source_en/              # 既有 matrixone 英文，不动
├── intelligence/           # ← 新增 intelligence 中文（demo 不做英文）
│   ├── conf.py             # 复用 matrixone 主题，下文给模板
│   ├── _static -> ../source/_static    # symlink，复用 CSS/JS/图片
│   ├── index.md            # 仿 matrixone hero + 入口卡
│   ├── getting-started/quickstart.md
│   ├── concepts/workspace.md
│   ├── tutorials/vector.md
│   ├── api/atomic-api.md
│   └── faq/product.md
└── Makefile                # 加一行 build target
```

**`intelligence/conf.py` 模板**（直接 from import + 覆盖品牌字段）：

```python
"""MatrixOne Intelligence 文档（demo 子站）

继承 matrixone 中文站的全部 Sphinx / MyST / Furo 配置，
只改产品名 / 标题 / copyright，主题色和扩展全部复用。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "source"))

from conf import *  # noqa: F401, F403, E402

# —— 内容字段：替换 ——
project = "MatrixOne Intelligence 文档"
html_title = "MatrixOne Intelligence 文档"
copyright = "2026, MatrixOne"

# —— 主题字段：暂不改，先和 matrixone 同色，验证完整性后再决定要不要换品牌色 ——
# 想换 intelligence 自己的紫蓝色调时，覆盖 html_theme_options 即可。
```

**`Makefile` 增量**（在现有 `html:` target 末尾加 2 行）：
```make
	uv run sphinx-build -a -b html intelligence $(BUILD)/intelligence-zh
	@echo "→ Intelligence (zh): $(BUILD)/intelligence-zh/index.html"
```

**根目录跳转**：现有的 `index.html` 写死跳到 `zh/` 或 `en/`。intelligence 子站演示时直接访问 `http://localhost:8000/intelligence-zh/` 即可，不需要联动跳转。**3 套站之间的导航关系，留给生产阶段**（README 里已经标了多版本 / Redirect 是研发 TODO）。

### 复用清单（不要做拷贝，要做 symlink）

| 资产 | 路径 | 处理 |
|---|---|---|
| 全套 CSS | `source/_static/css/custom.css` (2284 行) | symlink `intelligence/_static -> ../source/_static`（**整目录 symlink**，等同于 source_en 的做法） |
| 全套 JS | `source/_static/js/*.js`（7 个，含 assistant / lang-switcher / topbar / breadcrumb / feedback / footer / mo-highlight） | 同上，symlink 一起带 |
| 图片 / 图标 | `source/_static/images/` | 同上 symlink；intelligence 自己的图片走 CDN（moc-docs 本来就是这模式），不需要往 `_static/images` 加 |
| Furo 主题选项 | `source/conf.py` 的 `html_theme_options` / `html_css_files` / `html_js_files` | 通过 `from conf import *` 自动继承，**零代码** |
| MyST 扩展配置 | `source/conf.py` 的 `myst_enable_extensions` / `suppress_warnings` | 同上自动继承 |

**不要复制**：
- `source/index.md` —— intelligence 的首页要重写（产品名、副标题、入口卡片对应不同的目录）
- `source/getting-started/`、`source/concepts/` 等内容目录 —— 那是 matrixone 的内容
- `source/conf.py` —— 用 `from conf import *` 而不是物理复制，未来 matrixone 调主题，intelligence 跟着更新

### 方案 B（重新分层，推荐生产阶段用）

如果以后想改成你脑中的"matrixone / intelligence 平级子项目"结构：

```
docs-demo/
├── matrixone/
│   ├── source/         # mv from docs-demo/source/
│   ├── source_en/      # mv from docs-demo/source_en/
│   └── ... (Makefile 子集 / conf.py 不动)
├── intelligence/
│   ├── source/
│   ├── source_en/
│   └── ...
└── Makefile            # 改成进每个子目录递归 build
```

工作量：**0.5–1 天**（移文件 + 重写 Makefile + 改 README 路径 + 验证 build）。

**demo 阶段不建议先做这个重构**，理由：
- 移目录会让 git diff 变成"改名 + 内容变更"两件事混在一起，PR 难评审
- matrixone demo 是 4 月 25 日刚收尾的，结构动一动会冲击未保存的工作（你现在就有未提交的 `Makefile` / `frontend/` 改动 —— 这些看起来是 memoria 项目的，不是 docs-demo 的，但说明你工作流上同时有几个项目在飞，少改少错）

---

## 6. 风险提醒

### Sphinx 不支持但可解的特性
| MkDocs 特性 | Sphinx/MyST 处理 |
|---|---|
| Material 顶部 tab 导航（`navigation.tabs`） | Furo 无对等。用左侧 toctree 替代。**用户体验有差异**，但产品类文档其实左侧导航更主流 |
| `content.action.edit`（每页右上"编辑"按钮） | Sphinx 有 `html_context = {"display_github": True, ...}`，不同主题实现不同。Furo 用 `source_repository` + `source_branch` 配置即可 |
| `print-site` 整站可打印 | Sphinx 有 `latex` / `epub` builder，可生成 PDF。Demo 阶段不做 |
| `mike` 多版本切换 UI | Sphinx 用 `sphinx-multiversion`（README 已标 P0 TODO）。Demo 阶段不做 |
| `pymdownx.tasklist` 复选框 | 仓库实际只有 3 处。MyST 的 `tasklist` 扩展支持，但 demo `conf.py` 没开。**精选迁移不会撞到**，全量迁移时在 `myst_enable_extensions` 里加 `"tasklist"` 即可 |

### 链接断裂风险
- **moc-docs 内部相对链接 → demo 后大量 404**：FAQs/sql-faqs.md 第 5 行就有 `[MySQL 兼容性列表](../Overview/mysql-compatibility.md)`。精选迁移时 Overview 不一定迁，链接会断。**保留 demo 现有的 `suppress_warnings = ["myst.xref_missing"]`** 兜底，并在显眼处加 `:::{tip} 完整文档见 docs.matrixorigin.cn/intelligence` 引导跳官网
- **moc-docs → matrixone 站的跨站链接**：FAQ-Product.md 里有大量指向 `https://docs.matrixorigin.cn/2.0.3/MatrixOne/...` 的绝对 URL。这些是有效的外链，**不会断，不需要处理**
- **`workflow api/` 目录改名后所有内部链接需要同步改**：迁移脚本里 sed 一刀就能解决

### 图片路径风险
- **几乎没有路径风险**：71/74 篇引用图片的文档走 CDN URL（`community-shared-data-1308875761.cos.ap-beijing.myqcloud.com/artwork/mocdocs/images/...`），迁过来 URL 不变就能渲染
- **唯一例外**：`workflow api/` 目录里的 8 篇 API 文档，部分用了 `./images/api-management-entry.png` 这种本地相对路径，且 `workflow api/images/` 是个独立 image 目录。迁移这块时需要：
  1. 目录改名 `workflow api` → `workflow-api`
  2. `images/` 子目录跟着搬
  3. 相对图片链接 `./images/x.png` 不需改（Sphinx 同样支持）
- **demo 阶段策略 B 只迁 1 篇 `workflow api/automic_api.md`**：这一篇要么没本地图（待 grep 确认），要么把 `images/` 整目录搬过来，工作量 5 分钟

### 内容风险
- **glossary.md 用了非常规 Markdown 表格**（行首带空格、不对齐），MyST 的表格解析比较严格，可能渲染不出来。**精选迁移不包含 glossary**，规避此风险
- **`Reference/Operators/operators/operators/` 三层重名嵌套**很怪，迁移到 Sphinx 的 `:doc:` 引用会很难写。**精选不迁 Reference**，规避

---

## 总结一句话

`moc-docs` 是一个"内容质量 OK、技术栈干净（MkDocs Material + 极少扩展 + 图片全 CDN）"的源仓库，迁到 docs-demo 的 Sphinx + MyST 几乎没有意外坑。**建议走策略 B：精选 5 篇 + symlink 复用 matrixone 主题，半天落地**。等 demo 通过、要做产线，再考虑全量迁移和重新分层。

需要我接下来按策略 B 真正动手时，等你点头。
