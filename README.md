# MatrixOne Documentation Site

基于 Sphinx + Furo 的多产品文档站点，支持中英双语。

包含两个产品：

- **MatrixOne** — 一体化数据库，中英文档全量
- **MatrixOne Intelligence** — AI 原生多模态数据平台，中文 479 篇全量、英文 5 篇核心

## 快速启动

前置：macOS / Linux，已安装 [uv](https://github.com/astral-sh/uv)。

```bash
uv sync          # 装依赖
make html        # 构建 4 个站点到 build/html/
make serve       # 构建并启动本地服务 → http://localhost:8000
```

清理产物：

```bash
make clean
```

## URL 结构

| 路径 | 说明 |
|---|---|
| `/` | 产品选择页 |
| `/matrixone/` | 按浏览器语言跳到 `zh/` 或 `en/` |
| `/matrixone/zh/` | MatrixOne 中文站 |
| `/matrixone/en/` | MatrixOne 英文站 |
| `/intelligence/` | 同上自动跳转 |
| `/intelligence/zh/` | MatrixOne Intelligence 中文站（479 篇） |
| `/intelligence/en/` | MatrixOne Intelligence 英文站（核心 5 篇） |

## 项目结构

```
docs-demo/
├── pyproject.toml             # uv 依赖
├── Makefile                   # 4 路 sphinx-build + 产品 redirect + 产品选择页
├── README.md
│
├── matrixone/                 # matrixone 中文（主站点，主题资源在这里）
│   ├── conf.py
│   ├── _static/
│   │   ├── css/custom.css     # 品牌化 CSS（顶部 :root 集中色值）
│   │   └── js/                # topbar / breadcrumb / lang-switcher / icons / feedback / footer / assistant ...
│   └── （内容目录）
│
├── matrixone_en/              # matrixone 英文
│   ├── conf.py                # 继承 matrixone/conf.py，覆盖 language / html_title
│   ├── _static                # → symlink 到 ../matrixone/_static
│   └── （与 matrixone/ 一一对应）
│
├── intelligence/              # MatrixOne Intelligence 中文（迁自 moc-docs）
│   ├── conf.py
│   ├── _static                # → symlink 到 ../matrixone/_static
│   └── （479 篇内容 + 8 个 section index）
│
├── intelligence_en/           # MatrixOne Intelligence 英文（手译 5 篇）
│   ├── conf.py
│   ├── _static                # → symlink 到 ../source/_static
│   └── （主页 + Get-Started / Overview / workflow-api / FAQs 各 1 篇）
│
└── scripts/
    ├── migrate_from_mkdocs.py     # matrixone：从 mkdocs 迁
    ├── migrate_intelligence.py    # intelligence：从 moc-docs 迁
    └── build_picker.py            # 生成根目录产品选择页
```

产物目录：

```
build/html/
├── index.html                 # 产品选择页
├── matrixone/{index.html,zh/,en/}
└── intelligence/{index.html,zh/,en/}
```

## 技术栈

| 项 | 选型 |
|---|---|
| 静态站生成 | Sphinx 7.x |
| 内容格式 | Markdown（MyST） |
| 主题 | Furo |
| 扩展 | `myst-parser` / `sphinx-copybutton` / `sphinx-design` |
| 中文分词 | `jieba` |
| 包管理 | uv |

## 添加新产品

1. 新建 `<product>/` 目录（参考 `intelligence/`），放 `conf.py`、`index.md`、内容、symlink `_static -> ../source/_static`
2. 如果有英文版，再建 `<product>_en/`
3. 在 `Makefile` 的 `html:` 目标里加一行 `sphinx-build` 和一行 redirect HTML 输出
4. 在 `scripts/build_picker.py` 的 `HTML` 模板里加一张产品卡

## 添加新文档

直接在对应产品目录下加 `.md` 文件，并在所属 section 的 `index.md` 或主索引的 `{toctree}` 里挂上路径，重新 `make html`。

## 翻译覆盖

`source/_static/js/lang-switcher.js` 顶部两个常量控制右上角语言切换 pill：

```js
var HAS_EN = { matrixone: true };           // 英文全覆盖的产品
var PARTIAL_EN = {                          // 部分覆盖：仅在白名单页面显示 pill
  intelligence: [
    '', 'index.html',
    'Get-Started/quickstart.html',
    'Overview/matrixone-intelligence-introduction.html',
    'workflow-api/automic_api.html',
    'FAQs/FAQ-Product.html'
  ]
};
```

新翻译一篇文档时，把 `<rest>` 路径加进 `PARTIAL_EN` 数组对应产品；某产品翻译完全后，从 `PARTIAL_EN` 移除并加到 `HAS_EN`。

## 常见操作

| 任务 | 命令 |
|---|---|
| 本地预览 | `make serve` |
| 仅构建 matrixone 中文 | `uv run sphinx-build -a -b html matrixone build/html/matrixone/zh` |
| 仅构建 matrixone 英文 | `uv run sphinx-build -a -b html matrixone_en build/html/matrixone/en` |
| 仅构建 intelligence 中文 | `uv run sphinx-build -a -b html intelligence build/html/intelligence/zh` |
| 重新跑 intelligence 迁移脚本 | `uv run python scripts/migrate_intelligence.py` |
| 清理 | `make clean` |

## 说明

本项目是**演示原型**，不是生产文档站。文档助手按钮（右下角浮动 FAB）目前为占位回复，需要接 RAG 后端才能真正使用；多版本切换 / 全文搜索后端 / CI/CD 等生产能力均未覆盖。
