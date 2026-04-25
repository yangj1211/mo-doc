# MatrixOne 文档站 Demo

> 一个演示用的 Sphinx 文档站，用于向研发和老板表达**"我期望的文档站长什么样"**。
> 不是生产项目，是原型。

视觉上对齐 MatrixOne 官网（`#004af0` → `#31edff` 蓝青渐变）、
交互上模拟一个文档助手侧边抽屉。

---

## 快速启动

前置：macOS/Linux，已安装 [uv](https://github.com/astral-sh/uv)。

```bash
uv sync          # 装依赖（约 10 秒，首次）
make html        # 构建静态页面到 build/html
make serve       # 构建并启动本地服务 → http://localhost:8000
```

清理产物：`make clean`

---

## 看点（给老板看）

打开 `http://localhost:8000` 依次感受：

- [ ] **首页**：蓝青渐变标题 + 副标题 + 6 张入口卡片（hover 有上抬 + 边框变主色）
- [ ] **产品概述**（真实迁移）：进入 overview 看"核心特性 / 架构设计 / 对比"三组分区，架构图从 CDN 加载
- [ ] **版本发布**（真实迁移）：进入 release-notes，看 33 个版本倒序表格，点任一版本查看真实发布报告
- [ ] **常见问题**（真实迁移）：deployment-faqs 里的 Linux / macOS Tab 切换（MkDocs `=== "tab"` 已转为 sphinx-design `tab-set`）
- [ ] **5 分钟上手**（demo 样本）：有序步骤 + 代码块带复制按钮 + tip / warning / 下一步引导卡片
- [ ] **SQL 参考**（demo 样本）：参数表 / 错误码表、3 个带输出的 sql 示例
- [ ] **右下角助手按钮**：蓝紫渐变圆形 → 点击滑出抽屉 → 输入任意文字 → 收到占位回复
- [ ] **语言切换**：文章右上角（暗色按钮旁）的 pill，中文站 `EN` / 英文站 `中文`，URL 前缀互换，保留路径和 hash
- [ ] **暗色模式**：右上角月亮切换，代码块/表格/卡片全部自动适配
- [ ] **搜索 + 中文分词**：搜索 "快照"/"分支"/"HTAP"/"事务"/"架构" 能命中多篇真实文档

---

## 哪些是演示占位（不要当真）

| 位置 | 状态 | 说明 |
|------|------|------|
| 右下角助手按钮 | **UI only** | 发送后固定回复"助手后端开发中"，无真实 LLM/RAG |
| 页面中 `<a href="#">` 链接 | **占位** | 安全配置、在线沙箱、DROP/SHOW SNAPSHOT 等为空链接 |
| 首页 4 张 demo 卡（getting-started / concepts / sql-reference / troubleshooting） | **样本** | 每篇 500-1500 字示意，用于展示各类文档样式 |
| 迁移内容（overview / release-notes / faqs） | **真实** | 从官网 `matrixorigin.io.cn` 搬过来，共 61 篇；FAQ 里指向未迁移章节的内部链接会 404 |
| 英文站的翻译质量 | **AI 一次翻译** | 61 篇技术术语准确但措辞未经人工校对；产品文案（口号 / 营销语）质量一般，需技术写作团队过一遍 |
| 搜索 | **Furo 默认** | 无向量检索、无打分、无热度统计 |
| 多版本 | **未做** | 生产需要另外接 `sphinx-multiversion` |
| PDF / EPUB 导出 | **未做** | Sphinx 原生支持，按需开启 `latex` / `epub` builder |
| CI/CD | **未做** | 本地 `make` 即用，无 GitHub Actions / 预览部署 |

---

## Demo 覆盖对照表

| 文档站能力 | Demo 覆盖情况 |
|-----------|--------------|
| 信息架构（首页入口 → 分类 → 文章） | ✅ 6 张入口卡片 + 左侧 toctree 导航 |
| 真实内容验证（非 demo 手写） | ✅ 61 篇从官网 MkDocs 搬过来：release-notes 33 + overview 25 + faqs 3 |
| 迁移工具链（MkDocs → MyST） | ✅ 语法 99% 兼容，实测转换成本极低，方法见下文"迁移经验" |
| 品牌视觉（色、渐变、圆角、阴影） | ✅ 取自官网，CSS 变量集中管理 |
| 内容类型：操作指南 | ✅ `quickstart.md` |
| 内容类型：概念讲解 | ✅ `data-branch.md` |
| 内容类型：SQL / API 参考 | ✅ `snapshot.md` |
| 内容类型：FAQ | ✅ `faq.md` |
| 提示框（tip / warning / note / seealso） | ✅ 每种至少出现一次 |
| 代码块 + 复制按钮 + 高亮 | ✅ `sphinx-copybutton` |
| 表格（参数、错误码、对比） | ✅ 自定义样式：无边框 / 圆角 / 行 hover |
| 响应式（桌面 / 移动端） | ✅ Furo 原生 + 抽屉 mobile 全屏 |
| 暗色模式 | ✅ 品牌色双套 + 自动切换 |
| 中英双语 | ✅ `source/` + `source_en/` 并行构建，侧边栏语言 pill 切换 |
| 前端搜索 | ✅ Furo 默认，中文分词 |
| 文档助手浮动按钮（UI） | ✅ FAB + 抽屉 + 消息气泡 |
| 文档助手后端 | ❌ 占位回复 |
| 多版本 | ❌ 未覆盖 |
| 全文搜索后端（Algolia/向量） | ❌ 未覆盖 |
| API 从代码自动生成（`autodoc`） | ❌ 未覆盖（demo 用手写 md） |
| 版本化 URL / Redirect | ❌ 未覆盖 |

---

## 研发接手 TODO

产品阶段（演示完之后）要做成生产文档站，研发至少需要补：

### P0（影响能不能上线）
- [ ] **内容生产流程**：当前 4 篇是手写，生产需要和技术写作团队对接内容仓库或 CMS
- [ ] **文档助手后端**：接入 RAG 服务（embedding + 向量检索 + LLM 回答），前端契约只需改 `assistant.js` 里的 `REPLY` 逻辑为真实 `fetch('/api/assistant')`
- [ ] **真实链接**：替换所有 `<a href="#">` 占位链接，或引入 `sphinx-needs` / `intersphinx` 做跨文档引用
- [ ] **多版本**：引入 `sphinx-multiversion`（注意：与 Sphinx 9 不兼容，需锁 Sphinx 7.x）或自研版本切换
- [ ] **多语言工作流升级**：当前中英各一套独立 Markdown 文件，改动时需同步两边。生产建议切到 `sphinx-intl` + `.po` 以主语言为源、翻译文件做差分；或接入 Crowdin 做协作翻译

### P1（体验提升）
- [ ] **更强的搜索**：Algolia DocSearch / Meilisearch / 向量检索，替换 Furo 内置前端搜索
- [ ] **版本切换 UI**：右上角加 "v2.x / v3.x" 下拉（Furo 支持 `announcement` 和自定义 sidebar 模板）
- [ ] **"反馈"按钮**：每页底部加 "这篇文档对你有帮助吗？" 收集 NPS
- [ ] **访问统计**：接 PostHog / GA4（和 `assistant.js` 同样的挂载方式）
- [ ] **自动化**：GitHub Actions 构建 + Vercel / Cloudflare Pages 预览部署

### P2（锦上添花）
- [ ] **API Playground**：嵌入可在线运行 SQL 的沙箱（iframe 嵌官网沙箱即可）
- [ ] **深色代码块主题切换**：让用户自选 Dracula / GitHub Dark
- [ ] **目录大纲右侧浮动**（Furo 已自带，可定制排版）
- [ ] **AI 生成示例**：助手可以回写可复制的 SQL，结合 copybutton

---

## 项目结构

```
docs-demo/
├── pyproject.toml             # uv 管理的依赖（sphinx 7.x + furo + myst + copybutton + design + jieba）
├── Makefile                   # html 一次构建 zh + en + 根目录自动跳转 / serve / clean
├── README.md                  # 本文件
├── source/                    # 中文源（主）
│   ├── conf.py                # Sphinx 配置（品牌色、MyST 扩展、zh_CN、jieba 分词）
│   ├── index.md
│   ├── _static/
│   │   ├── css/custom.css     # 品牌化定制，色值/圆角/阴影集中在顶部 :root
│   │   ├── js/assistant.js    # 助手按钮 + 抽屉（zh/en 双语，自挂载到 body）
│   │   └── js/lang-switcher.js # 语言切换 pill（注入 Furo theme-toggle 容器，挨着暗色按钮）
│   ├── getting-started/quickstart.md
│   ├── concepts/data-branch.md
│   ├── sql-reference/snapshot.md
│   └── troubleshooting/faq.md
└── source_en/                 # 英文源
    ├── conf.py                # 继承 source/conf.py，只覆盖 language / html_title
    ├── _static                # → symlink 到 ../source/_static（共享静态资源）
    ├── index.md               # 和中文版结构一一对应
    ├── getting-started/quickstart.md
    ├── concepts/data-branch.md
    ├── sql-reference/snapshot.md
    └── troubleshooting/faq.md
```

**产物结构**：

```
build/html/
├── index.html     # 根目录自动跳转：浏览器语言 zh-* → /zh/，其余 → /en/
├── zh/            # 完整中文站
└── en/            # 完整英文站
```

---

## 技术选型（已定，建议研发沿用）

| 项 | 选型 | 原因 |
|----|------|------|
| 静态站点生成 | Sphinx 7.x | 行业标准，生态完整；避开 9.x 是因为 `sphinx-multiversion` 未适配 |
| 内容格式 | Markdown（MyST） | 学习曲线低，对写作团队友好；保留 rST 能力作为 fallback |
| 主题 | Furo | 现代、暗色模式原生支持、可定制度适中 |
| 扩展 | `myst-parser` / `sphinx-copybutton` / `sphinx-design` | 覆盖 95% 文档场景 |
| 包管理 | uv | 比 pip 快 10 倍，lockfile 体验接近 cargo |

---

## 从 MkDocs 迁移的经验（给全量迁移做参考）

本 demo 从官网 `matrixorigin.io.cn/docs/MatrixOne/` 迁了 3 个目录（61 篇）来验证可行性：

| 迁移工作 | 实际工作量 |
|---------|-----------|
| 语法兼容性扫描（`!!!` / `===` / `???` / `<font>` / mermaid） | 10 分钟（几乎全兼容，只 1 个 FAQ 文件有特殊语法） |
| 原样 `cp -R` | 秒级 |
| MkDocs 专属语法手工转换 | 1 个 `=== "tab"` → `{tab-set}`、1 个 `!!! note` → `:::{note}`（5 分钟） |
| 老版本 RN 里的 `***` 分隔线（docutils 不允许紧跟标题） | 1 个 sed 搞定（2 分钟） |
| 跨目录链接大小写（`Overview/` → `overview/`） | 1 个 sed（1 分钟） |
| 未迁移目录的 broken link | `suppress_warnings = ["myst.xref_missing"]`（全量迁移时取消） |

**结论**：MkDocs MD → MyST MD 转换成本远低于我之前估的 1-2 周，大概 **2-3 天**就能搬完 630 篇，前提是：
- 先写一个 Python 脚本批量处理 `=== / !!! / ???` 三种语法
- 图片路径保持相对路径不变（`_static/images` 布局和 MkDocs 一致）
- 允许先留 broken link、后续分批修复

## 关键实现备忘（踩过的坑，研发别再踩）

1. **不要继承 Furo 的 `layout.html`** — Furo 的 `layout.html` 本身是一个 "请不要继承我"的报错占位页。需要注入 site-wide UI 用 JS 自挂载到 `document.body`（`assistant.js` 的做法）。
2. **`:::{div}` 会把内部 h1 降级成 `<p class="rubric">`** — 会丢失 Sphinx 的文档标题语义。需要给 h1 加 class 时用 attrs_block `{.class-name}` 写在 `#` 标题前，class 会打到外层 `<section>` 上。
3. **BNF 风格的 `{ A | B | C }` 语法模板让 Pygments SQL lexer 报 warning** — 已在 `conf.py` 设 `suppress_warnings = ["misc.highlighting_failure"]` 压掉。
4. **品牌色来源** — 不是拍脑袋定的，从 `official_website` 的 `tokens.css` 和 `index.css` 提取（`#004af0` / `#31edff` / `#8b7cf0` / `#142140`）。修改请同步更新官网。
