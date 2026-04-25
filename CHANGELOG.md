# CSS 精细化调优 Changelog

---

## Round 2（最终精修）：代码块转浅色 Snowflake 风 + 方言高亮 + 关联元素

涉及文件：
- `source/_static/css/custom.css`（代码段 §4 完整重写 + §7/§8/§9/§10 局部调整）
- `source/_static/js/mo-highlight.js`（**新文件**：MatrixOne 方言关键字二次高亮）
- `source/_static/js/topbar.js`（logo 去字标，改用 "MatrixOne + Docs" 形式）
- `source/conf.py`（`html_js_files` 新增 `js/mo-highlight.js`）

### 2.1 代码块：深色 → 浅色 Snowflake / GitHub 风

| 对象 | 原 | 新 |
|------|----|----|
| 背景 | `#0F172A`（深蓝黑） | `#F6F8FA`（GitHub 冷灰，略带蓝调） |
| 边框 | 全无 | **左侧 3px solid `#3B82F6`** 品牌竖边；其他三边无 |
| 圆角 | 8px 全边 | `0 8px 8px 0`（左侧贴平竖边） |
| 阴影 | 无 | 无 |
| padding | `28px 18px 16px`（顶部为语言标签留空） | `20px 24px` |
| margin | — | `20px 0` |
| 字号 | `13.5px` | `14.5px` |
| 行高 | `1.6` | `1.7` |
| 字体 | JetBrains Mono 栈 | 同；新增 `font-feature-settings: "liga" 1` 启用连字 |
| 默认字色 | `#e2e8f0`（暗色用） | `#24292F`（GitHub 深灰黑） |

### 2.2 语法高亮：GitHub 浅色配色

| Pygments 类 | 原（深色主题） | 新 |
|------------|---------------|----|
| `.k/.kc/.kd/.kn/.kp/.kr/.kt`（关键字） | `#C4B5FD` 淡紫 | **`#0969DA` GitHub 蓝 + `font-weight: 600`** |
| `.s/.s1/.s2/...`（字符串） | `#67E8F9` 淡青 | `#0A3069` 深蓝 |
| `.m/.mi/.mf/...`（数字） | `#FCD34D` 淡橙 | `#0550AE` 中蓝 |
| `.c/.c1/.cm/...`（注释） | `#64748B` + 斜体 | `#6E7781` + 斜体 |
| `.o/.ow`（操作符） | —（无覆盖） | **新增**：`#CF222E` 橙红 |
| `.nv/.vi/.vg`（变量） | —（无覆盖） | **新增**：`#953800` 深橙 |
| `.nf/.fm`（函数名） | —（无覆盖） | **新增**：`#8250DF` 紫 |

### 2.3 MatrixOne 方言关键字（**新功能**）

Pygments SQL / bash lexer 不识别 `SNAPSHOT` / `CLONE` / `DATA BRANCH` 等 MatrixOne 专有词。新增：

- `source/_static/js/mo-highlight.js`：DOMContentLoaded 后扫描 `.highlight-sql / .highlight-mysql / .highlight-bash / .highlight-zsh / .highlight-text` 代码块，用正则把方言关键字包成 `<span class="mo-keyword">`。
  - **多词短语**（先匹配长的）：`FOR SYSTEM_TIME`、`RESTORE FROM SNAPSHOT`、`CREATE / DROP SNAPSHOT`、`CREATE / DROP / ALTER PITR`、`SHOW SNAPSHOTS / PITRS`、`WHEN CONFLICT`、`MERGE INTO`、`DATA BRANCH`、`CREATE / DROP BRANCH`
  - **单词级**：`SNAPSHOT(S)`、`CLONE(S)`、`BRANCH(ES)`、`PITR(S)`、`RESTORE`、`VECF32/64`、`CDC`、`HTAP`、`HSTAP`、`DATABRANCH`
  - 正则支持跨 span 匹配（Pygments 可能把相邻 token 分成多个 span，脚本里用 `(?:\s|<[^<>]*>)+` 作分隔符）
- CSS 新增 `.mo-keyword { color: #8250DF; font-weight: 600; }`，`!important` 覆盖 Pygments 默认色

### 2.4 去掉代码块语言标签

上一轮用 `::before` 注入的 `bash` / `sql` / `python` 等左上角语言标签**全部删除**。相关 CSS（`.highlight-bash > .highlight::before` 及 17 种语言）一并删。

### 2.5 复制按钮克制化

| 属性 | 原 | 新 |
|------|----|----|
| 位置 | 默认 Furo / copybutton 样式 | `position: absolute; top: 12px; right: 12px` |
| 尺寸 | — | `24px × 24px`，`padding: 4px` |
| 默认样式 | 含背景、边框 | `background: transparent; border: none; color: #6E7781; opacity: 0.8` |
| hover | — | `background: rgba(0,0,0,.06); color: #24292F; opacity: 1` |
| 成功态（`.success`） | — | `color: #3B82F6`（主色），由 sphinx-copybutton 自动切换 |

### 2.6 行内 code：GitHub 风同色系

| 属性 | 原 | 新 |
|------|----|----|
| 背景 | `#F1F5F9` | `#F6F8FA`（和代码块同色） |
| 文字 | `#475569` | `#24292F` |
| 其他（字号 0.875em / padding 2px 6px / radius 4px / 字体 JetBrains Mono） | 同 | 不变 |

### 2.7 顶部导航 tab：当前项改为"蓝字 + 下划线"

| 状态 | 原 | 新 |
|------|----|----|
| 默认 | `#4B5563` / 500 | `#374151` / 500 / 14px |
| hover | `#1F2937` | `#1F2937` |
| **当前项** | 灰字 + 主色下划线 | **`#3B82F6` 蓝字 + 主色下划线 + 500**（文字也上色了，更清晰） |
| 项间距 | `gap: 4px` + 每个 tab `padding: 0 12px` | `gap: 32px` + `padding: 0`（项间距拉开，更有呼吸） |

### 2.8 Logo 区简化

`[logo] MatrixOne | DOCUMENTATION`（竖线分隔的大写字标）→ **`[logo] MatrixOne Docs`**（空格分隔）

- `.mo-topbar__title` "MatrixOne"：`16px / 600 / #111827`
- `.mo-topbar__docs` "Docs"（zh: "文档"）：`14px / 400 / #6B7280`
- 删掉 `.mo-topbar__wordmark` 的竖线 + uppercase + letter-spacing
- `topbar.js` 也同步改了 DOM：`mo-topbar__wordmark` → `mo-topbar__docs`，i18n 字段 `wordmark` → `docsLabel`

### 2.9 左侧侧边栏当前项调整

| 属性 | 原 | 新 |
|------|----|----|
| 背景 | `#EFF6FF` | 同 |
| 文字 | `#3B82F6`（`--mo-brand-soft`） | **`#2563EB`**（`--mo-brand-sidebar`，略深，和右 TOC 区分） |
| 字重 / 左竖条 | 400 / 无 | 同 |

### 2.10 右侧 TOC（页面大纲）—— **新增样式**

之前没有专门规则，Furo 默认当前项显示为品牌原色。现在：

- 默认 `a`：`#4B5563` / 400
- hover：`#1F2937`
- **当前（`.scroll-current` / `.current`）**：`#3B82F6` / **500（不加粗到 600）** / 左侧 `2px solid #3B82F6` 竖条
- 暗色模式对应 `#6b8cff`

### 2.11 sphinx-design tab-set（Linux / macOS 切换）—— Segment 风格

原 sphinx-design 默认样式是"整行底部下划线"风格。现在改成 iOS / macOS Segment Control 的胶囊组：

| 组件 | 样式 |
|------|------|
| 容器 `.sd-tab-set` | `inline-flex` / `width: auto` / `bg: #F1F5F9` / `padding: 4px` / `radius: 8px` |
| tab 标签 | `padding: 6px 16px` / `font-size: 14px` / `font-weight: 500` / `radius: 6px` |
| 默认 tab | 透明底 / `color: #64748B` |
| **激活 tab** | `bg: #FFFFFF` / `color: #1F2937` / `box-shadow: 0 1px 2px rgba(0,0,0,0.05)` |
| 非激活 hover | `color: #374151` |
| transition | `all 0.15s ease` |
| 暗色模式 | 容器 `#1a2338`、激活 `#0f172a` 底 + 浅字 |

### 2.12 暗色模式代码块

| 属性 | 值 |
|------|----|
| 背景 | `#161B22` |
| 左竖边 | `#3B82F6`（保持品牌色一致） |
| 默认字色 | `#E6EDF3` |
| 关键字 | `#79C0FF` + 600 |
| 方言紫 | `#D2A8FF` |
| 字符串 | `#A5D6FF` |
| 数字 | `#79C0FF` |
| 注释 | `#8B949E` + 斜体 |
| 操作符 | `#FF7B72` |
| 行内 code | `bg: #161B22` / `color: #E6EDF3` |
| 复制按钮 hover | `bg: rgba(255,255,255,.08)` / `color: #E6EDF3` |

### 2.13 新增设计 Token（`:root`）

`--mo-brand-sidebar` / `--mo-ink-500` / `--mo-ink-800` / `--mo-ink-300` / `--mo-surface-code` / `--mo-code-keyword` / `--mo-code-dialect` / `--mo-code-string` / `--mo-code-number` / `--mo-code-comment` / `--mo-code-operator` / `--mo-code-variable` / `--mo-code-function`。

---

## Round 1：从"饱满"往"克制"收（初版）

本次只改 `source/_static/css/custom.css`，目标：从"饱满"往"克制"收。布局结构、Hero、
FAB、logo 均未动。

---

## 1. 顶部导航链接：饱和品牌色 → 中深灰

| 选择器 | 改动 |
|--------|------|
| `.mo-topbar__tab` | `color: #4B5563`（原 `--color-foreground-secondary`）；`font-weight: 500`；`font-size: 14px` |
| `.mo-topbar__tab:hover` | `color: #1F2937`（原 `--color-foreground-primary`） |
| `.mo-topbar__tab--active` | `color: #1F2937`（原 `var(--mo-primary)`，即蓝色）；`border-bottom-color` 保留品牌蓝 |

只有"下划线"用品牌色，文字全部灰。

---

## 2. H1 标题收敛

| 选择器 | 改动 |
|--------|------|
| `article h1` | 新增完整规则：`font-size: 30px` / `font-weight: 600` / `color: #111827` / `letter-spacing: -0.02em` / `margin: 0 0 24px` |

原来是 Furo 默认（约 40px/700），现在是 30px/600。

---

## 3. 标题阶梯 H1–H4

| 选择器 | 改动 |
|--------|------|
| `article h2` | 新增：`22px / 600 / #111827 / margin: 48px 0 16px` |
| `article h3` | 新增：`17px / 600 / #1F2937 / margin: 32px 0 12px` |
| `article h4` | 新增：`15px / 600 / #374151 / margin: 24px 0 8px` |
| `article :is(h1,h2,h3,h4) .headerlink` | 默认 `opacity: 0`，hover 标题才出来 |

字号、字重、颜色、间距四维递减，层级清晰。

---

## 4. 代码块：米黄 → 深蓝黑（方案 B）

| 选择器 | 改动 |
|--------|------|
| `.highlight` | 原有 `box-shadow` 删除；保留深色 `--mo-code-bg: #0F172A` |
| `.highlight pre` | `padding: 28px 18px 16px`（上方留空给语言标签，原 `16px 18px`） |
| `[class^="highlight-"] > .highlight::before` | 新增：左上角语言标签（`#64748B` / 11px / uppercase / 等宽字体） |
| `.highlight-{bash,sql,python,...}::before` | 新增：每种语言对应的 `content` |
| `.highlight .k / .kc / .kd / ...` | 新增：关键字 `#C4B5FD` |
| `.highlight .s / .s1 / .s2 / ...` | 新增：字符串 `#67E8F9` |
| `.highlight .m / .mi / .mf / ...` | 新增：数字 `#FCD34D` |
| `.highlight .c / .c1 / .cm / ...` | 新增：注释 `#64748B` + `font-style: italic` |
| `.highlight button.copybtn` | `top: 6px; right: 6px`（和语言标签错位） |

---

## 5. 行内 code：蓝底蓝字 → 冷灰底深灰字

| 选择器 | 改动 |
|--------|------|
| `code.literal, p code, li code, td code, th code` | `font-family: JetBrains Mono` 栈；`font-size: 0.875em`；`padding: 2px 6px`；`border-radius: 4px`；`background: #F1F5F9`（原 `#e8efff`）；`color: #475569`（原 `#1d49e7`） |

视觉不再像按钮，只是正文里的轻标记。

---

## 6. 侧边栏当前项：三种强调手段 → 一种

| 选择器 | 改动 |
|--------|------|
| `.sidebar-tree .reference` | 默认 `color: #4B5563`；`font-weight: 400`；`padding: 8px 12px`；`border-radius: 6px` |
| `.sidebar-tree .reference:hover` | `background: #F8FAFC`；`color: #1F2937` |
| `.sidebar-tree a.current` | **唯一强调**：`background: #EFF6FF`；`color: #3B82F6`；`font-weight: 400`；`border-left: none !important` |
| `.sidebar-tree a.current strong` | `font-weight: 400`（去掉 Furo 默认加粗） |

之前是"加粗 + 变色 + 左竖条 + 大号字"叠加，现在只剩"淡底 + 主色字"。

---

## 7. 留白与呼吸感

| 选择器 | 改动 |
|--------|------|
| `article[role="main"]` | 新增：`max-width: 800px`；`margin: 0 auto`；`padding: 0 48px` |
| `article p` | `margin: 0 0 1.25em`；`line-height: 1.7` |
| `article ul, article ol` | `margin: 0 0 1.25em`；`padding-left: 1.5em` |
| `article li + li` | `margin-top: 0.5em` |
| `article h2` | `margin-top: 48px`（见 #3） |
| `.sidebar-tree .reference` | `padding: 8px 12px`（见 #6） |

内容区居中 800px，两侧 48px 内边距，段落、列表、标题之间的 margin 统一收紧。

---

## 8. 搜索框克制化

| 选择器 | 改动 |
|--------|------|
| `.mo-topbar__search` | `max-width: 480px`（原 `560px`） |
| `.mo-topbar__search input` | `border-radius: 8px`（原 `10px`）；`background: #F8FAFC`；`border: 1px solid #E2E8F0` |
| `.mo-topbar__search input::placeholder` | `color: #94A3B8` |
| `.mo-topbar__search input:focus` | `border-color: #3B82F6`；`box-shadow: 0 0 0 3px rgba(59,130,246,.12)` |
| `.mo-topbar__search kbd` | `font-family: JetBrains Mono` 栈；字色和边框收为中性灰 |

---

## 9. 表格精致化

| 选择器 | 改动 |
|--------|------|
| `table.docutils` | `box-shadow: none`（原 `var(--mo-shadow-sm)`）；`border-radius: 8px` |
| `table.docutils thead th` | `background: #F8FAFC`；`color: #475569`；`font-weight: 500`；`font-size: 13px`；`text-transform: uppercase`；`letter-spacing: 0.05em` |
| `table.docutils tbody td` | `border-bottom: 1px solid #F1F5F9`（原 `--color-background-border`，更淡） |
| `table.docutils tbody tr:hover` | `background: #FAFBFC`（原 `rgba(0,74,240,.035)`，去蓝调） |
| `table.docutils tbody td:first-child` | **新增**：`font-family: JetBrains Mono` 栈；`font-size: 0.88em`（参数名列用等宽） |

---

## 其他附带调整

- `blockquote` 去掉了原有的"左竖条主色 + 蓝紫渐变背景"，改成细灰边 + 正文次要色。
- `.admonition` 去 `box-shadow`，`border-left-width` 从 4px 收到 3px。
- `.sd-card` hover 去掉 `translateY(-3px)` 抬升动作，只留边框变色 + 轻阴影。
- `.sidebar-brand-text` 的渐变文字保留（还在 sidebar brand 生效位置之外，规则不会触发，保留没副作用）。
- 新增 CSS 变量：`--mo-ink-{300..900}`、`--mo-surface-{50, 100, 150, faint}`、`--mo-code-{kw, str, num, cmt}`、`--mo-brand-soft`、`--mo-font-mono`。所有新颜色对齐了 Tailwind gray/slate 色板，方便研发后续对齐设计稿。

## 不改动的部分

- Hero 标题的蓝青渐变文字
- FAB 圆形按钮 + 抽屉
- logo + "MatrixOne" 字标
- 首页 6 张入口卡片的结构
- 顶栏的双行布局和 tab 导航的结构
- 语言 pill
