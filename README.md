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

```
docs-demo/
├── pyproject.toml
├── Makefile                       # 根入口:委派给两个产品 + 产品选择页
├── README.md
│
├── matrixone/                     # MatrixOne 产品
│   ├── conf.py                    # 中英共用,SPHINX_LANG 切品牌标题
│   ├── Makefile                   # html / html-zh / html-en
│   └── source/
│       ├── _static/               # 中英共享的主题资源
│       │   ├── css/custom.css     # 品牌化 CSS(顶部 :root 集中色值)
│       │   └── js/                # topbar / breadcrumb / lang-switcher / version-switcher / icons / ...
│       ├── _templates/            # 中英共享的 Jinja 模板覆盖
│       ├── zh/                    # 中文内容
│       └── en/                    # 英文内容
│
├── matrixone-intelligence/        # MatrixOne Intelligence 产品(同形)
│   ├── conf.py                    # 继承 matrixone/conf.py,覆盖品牌
│   ├── Makefile
│   └── source/
│       ├── _static                # → symlink 到 ../../matrixone/source/_static
│       ├── _templates             # → symlink 到 ../../matrixone/source/_templates
│       ├── zh/                    # 479 篇 + 8 个 section index
│       └── en/                    # 主页 + Get-Started / Overview / workflow-api / FAQs 各 1 篇
│
└── scripts/
    ├── migrate_from_mkdocs.py     # matrixone:从 mkdocs 迁
    ├── migrate_intelligence.py    # matrixone-intelligence:从 moc-docs 迁
    └── build_picker.py            # 生成根目录产品选择页
```

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

1. 新建 `<product>/` 目录,按 matrixone 的形状填:`conf.py`、`Makefile`、`source/{_static,_templates,zh,en}/`。`_static` / `_templates` 可以用 symlink 指到 matrixone 的对应目录复用主题。
2. `conf.py` 推荐 `from conf import *`(像 matrixone-intelligence 那样)继承 matrixone 的全部配置,只覆盖品牌字段。
3. 根 `Makefile` 的 `html` 目标加一行 `$(MAKE) -C <product> html`,redirects 段加一段 `<product>/index.html` 写入。
4. `scripts/build_picker.py` 的 `HTML` 模板里加一张产品卡。

## 添加新语言

1. `<product>/source/<lang>/` 新建子目录,放进对应语言的全部内容。
2. `<product>/Makefile` 加 `html-<lang>:` 目标,把 `SPHINX_LANG` 和 `-D language=` 传进去。
3. `source/_static/js/lang-switcher.js` 加新语言的 LABEL / 路径解析正则。

## 添加新文档

直接在 `<product>/source/<lang>/` 下加 `.md` 文件,并在所属 section 的 `index.md` 或主索引的 `{toctree}` 里挂上路径,重新 `make html`。

## 翻译覆盖

`matrixone/source/_static/js/lang-switcher.js` 顶部两个常量控制右上角语言切换 pill:

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
