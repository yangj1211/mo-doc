# MatrixOne Documentation Site

基于 Sphinx + Furo 的多产品文档站点,支持中英双语。

包含两个产品:

- **MatrixOne** — 一体化数据库,中英文档全量
- **MatrixOne Intelligence** — AI 原生多模态数据平台,中文 479 篇全量、英文 5 篇核心

## 快速启动

前置:macOS / Linux,已安装 [uv](https://github.com/astral-sh/uv)。

```bash
uv sync                      # 装依赖
make html                    # 构建 4 个站点到 build/html/
make serve                   # 构建并启动本地服务 → http://localhost:8000
```

只构建一个产品:

```bash
cd matrixone && make html       # zh + en
cd matrixone && make html-zh    # 只中文
cd matrixone && make html-en    # 只英文
```

matrixone-intelligence 同形:`cd matrixone-intelligence && make html / html-zh / html-en`。

清理:

```bash
make clean                   # 删根目录 build/
```

## URL 结构

| 路径 | 说明 |
|---|---|
| `/` | 产品选择页 |
| `/matrixone/` | 按浏览器语言跳到 `zh/` 或 `en/` |
| `/matrixone/zh/` | MatrixOne 中文站 |
| `/matrixone/en/` | MatrixOne 英文站 |
| `/matrixone-intelligence/` | 同上自动跳转 |
| `/matrixone-intelligence/zh/` | MatrixOne Intelligence 中文站(479 篇) |
| `/matrixone-intelligence/en/` | MatrixOne Intelligence 英文站(核心 5 篇) |

## 项目结构

**主题共享、内容独立**:所有产品共用 `_shared_theme/`(CSS/JS/模板/Sphinx 配置基类),内容各自在 `<product>/source/{zh,en}/`。

```
docs-demo/
├── pyproject.toml
├── Makefile                       # 根入口:委派给每个产品 + 产品选择页
├── README.md
│
├── _shared_theme/                 # ★ 仓库唯一一份主题,所有产品继承
│   ├── conf_base.py               # 共享 Sphinx / MyST / Furo 配置基类
│   ├── _static/
│   │   ├── css/custom.css         # 全部样式(:root tokens + [data-product] 品牌槽)
│   │   ├── js/                    # topbar / breadcrumb / lang-switcher / version-switcher / icons / assistant / ...
│   │   └── images/                # logo 等共享资源
│   └── _templates/
│       └── page.html              # 覆盖 Furo page.html,给 <html> 注入 data-product
│
├── matrixone/                     # MatrixOne 产品
│   ├── conf.py                    # from conf_base import *,只声明产品维度
│   ├── Makefile                   # html / html-zh / html-en
│   └── source/
│       ├── zh/                    # 中文内容
│       └── en/                    # 英文内容
│
├── matrixone-intelligence/        # MatrixOne Intelligence 产品(同形)
│   ├── conf.py                    # 同样 from conf_base import *,product='intelligence' 走紫调
│   ├── Makefile
│   └── source/
│       ├── zh/                    # 479 篇 + 8 个 section index
│       └── en/                    # 主页 + Get-Started / Overview / workflow-api / FAQs 各 1 篇
│
└── scripts/
    ├── migrate_from_mkdocs.py     # matrixone:从 mkdocs 迁
    ├── migrate_intelligence.py    # matrixone-intelligence:从 moc-docs 迁
    ├── convert_admonitions.py     # MkDocs admonition / tab → MyST 批量转换
    └── build_picker.py            # 生成根目录产品选择页
```

**关键约定:**
- 主题层任何修改(CSS/JS/模板)只需改 `_shared_theme/`,所有产品自动同步
- 产品独有的品牌色通过 CSS 变量 + `[data-product="..."]` 选择器区分,不需要写两套样式
  - matrixone:蓝调(`:root` 默认)
  - matrixone-intelligence:紫调(`html[data-product="intelligence"]` 覆写 `--mo-primary` 等 token)
- 产品 `conf.py` 只放产品维度(产品名、`html_context.product`、独有 JS 文件等),Sphinx/MyST/扩展配置全在 `conf_base.py`

产物目录:

```
build/html/
├── index.html                     # 产品选择页
├── matrixone/{index.html,zh/,en/}
└── matrixone-intelligence/{index.html,zh/,en/}
```

## 技术栈

| 项 | 选型 |
|---|---|
| 静态站生成 | Sphinx 7.x |
| 内容格式 | Markdown(MyST) |
| 主题 | Furo |
| 扩展 | `myst-parser` / `sphinx-copybutton` / `sphinx-design` |
| 中文分词 | `jieba` |
| 包管理 | uv |

## 添加新产品

1. 新建 `<product>/` 目录,只放产品独有的东西:
   ```
   <product>/
   ├── conf.py
   ├── Makefile
   └── source/{zh,en}/
   ```
   主题资源全部沿用 `_shared_theme/`,**不需要复制 _static / _templates**。
2. `conf.py` 模板(参考 `matrixone/conf.py`):
   ```python
   import os, sys
   from pathlib import Path
   sys.path.insert(0, str(Path(__file__).parent.parent / "_shared_theme"))
   from conf_base import *

   _lang = os.environ.get("SPHINX_LANG", "zh_CN")
   project = "..." if _lang == "en" else "..."
   html_title = project
   language = _lang
   html_static_path = ["../_shared_theme/_static"]
   templates_path = ["../_shared_theme/_templates"]
   html_context = {"product": "<slug>"}     # 决定 CSS 走哪一套品牌色
   ```
3. 如果新产品要不同品牌色,在 `_shared_theme/_static/css/custom.css` 里加一段:
   ```css
   html[data-product="<slug>"] {
     --mo-primary:    #...;
     --mo-brand-soft: #...;
   }
   ```
4. 根 `Makefile` 的 `html` 目标加 `$(MAKE) -C <product> html`,redirects 段加 redirect HTML。
5. `scripts/build_picker.py` 的 `HTML` 模板里加产品卡。

## 添加新语言

1. `<product>/source/<lang>/` 新建子目录,放进对应语言的内容。
2. `<product>/Makefile` 加 `html-<lang>:` 目标,把 `SPHINX_LANG` 和 `-D language=` 传进去。
3. `_shared_theme/_static/js/lang-switcher.js` 加新语言的 LABEL / 路径解析正则。

## 添加新文档

直接在 `<product>/source/<lang>/` 下加 `.md` 文件,并在所属 section 的 `index.md` 或主索引的 `{toctree}` 里挂上路径,重新 `make html`。

## 翻译覆盖

`_shared_theme/_static/js/lang-switcher.js` 顶部两个常量控制右上角语言切换 pill:

```js
var HAS_EN = { matrixone: true };           // 英文全覆盖的产品
var PARTIAL_EN = {                          // 部分覆盖:仅在白名单页面显示 pill
  'matrixone-intelligence': [
    '', 'index.html',
    'Get-Started/quickstart.html',
    'Overview/matrixone-intelligence-introduction.html',
    'workflow-api/automic_api.html',
    'FAQs/FAQ-Product.html'
  ]
};
```

新翻译一篇文档时,把 `<rest>` 路径加进 `PARTIAL_EN` 数组对应产品;某产品翻译完全后,从 `PARTIAL_EN` 移除并加到 `HAS_EN`。

## 版本管理

当前只有 `latest` 一个版本。顶部版本切换器是 UI 占位,下拉里只显示 latest 加一段"历史版本归档功能开发中"的提示文字。

未来扩展思路(本仓库不实现):

- 单源构建多个版本 → 输出到 `build/html/<product>/<version>/<lang>/`
- 历史版本归档目录 `archive/<product>/<version>/`,直接拷成静态产物
- 版本切换器从静态 `versions.json` 读列表

研发上线时再根据真实版本管理需求选定方案。

## 常见操作

| 任务 | 命令 |
|---|---|
| 本地预览全部 | `make serve` |
| 只构建 matrixone | `cd matrixone && make html` |
| 只构建 matrixone 中文 | `cd matrixone && make html-zh` |
| 只构建 matrixone-intelligence 英文 | `cd matrixone-intelligence && make html-en` |
| 重新跑 matrixone-intelligence 迁移脚本 | `uv run python scripts/migrate_intelligence.py` |
| 清理 | `make clean` |

## 说明

本项目是**演示原型**,不是生产文档站。文档助手按钮(右下角浮动 FAB)目前为占位回复,需要接 RAG 后端才能真正使用;多版本切换、全文搜索后端、CI/CD 等生产能力均未覆盖。
