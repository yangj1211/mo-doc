/* MatrixOne 文档助手 —— 假数据驱动的智能演示
   - 所有"智能"都是关键词匹配 + 预置回答；不接真实后端
   - 视觉/交互模拟完整产品形态：流式输出 / 来源 / 跟进 / 反馈
   - 维护重点：DEMO_RESPONSES 关键词→回答；PAGE_SUGGESTIONS 路径→推荐问 */
(function () {
  'use strict';
  if (document.querySelector('.mo-fab')) return;

  /* =========================================================
     0. i18n & 文案
     ========================================================= */
  var LANG = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0 ? 'en' : 'zh';
  var I18N = {
    zh: {
      brand: 'MatrixOne 助手',
      welcomeTitle: 'MatrixOne 文档助手',
      welcomeSubtitle: '我可以帮你理解概念、生成 SQL、解释报错',
      suggestionHead: '不知道问什么？试试',
      sourceHead: '相关文档',
      followupHead: '你可能还想问',
      placeholder: '问我关于 MatrixOne 的任何问题...',
      sendLabel: '发送',
      closeLabel: '关闭',
      openLabel: '打开 MatrixOne 文档助手',
      attachLabel: '附加 SQL 报错（即将上线）',
      feedbackThanks: '感谢反馈',
      tagSep: '、'
    },
    en: {
      brand: 'MatrixOne Assistant',
      welcomeTitle: 'MatrixOne Docs Assistant',
      welcomeSubtitle: 'I can explain concepts, generate SQL, and decode errors',
      suggestionHead: 'Try asking',
      sourceHead: 'Related docs',
      followupHead: 'You might also want to ask',
      placeholder: 'Ask me anything about MatrixOne...',
      sendLabel: 'Send',
      closeLabel: 'Close',
      openLabel: 'Open MatrixOne docs assistant',
      attachLabel: 'Attach SQL error (coming soon)',
      feedbackThanks: 'Thanks for the feedback',
      tagSep: ' · '
    }
  };
  var T = I18N[LANG];

  /* =========================================================
     1. 推荐问题（按当前页路径片段命中）
     ========================================================= */
  var PAGE_SUGGESTIONS = LANG === 'en' ? {
    '/sql-reference/snapshot': [
      'How do I create a table snapshot?',
      "What's the difference between snapshot and data branch?",
      'Does restoring from a snapshot overwrite live data?'
    ],
    '/sql-reference/': [
      'How does CREATE SNAPSHOT work?',
      'Is MERGE INTO supported?',
      'How does EXPLAIN output differ from MySQL?'
    ],
    '/concepts/data-branch': [
      'Are data branches like Git branches?',
      'How much storage does a branch take?',
      'How are merge conflicts resolved?'
    ],
    '/concepts/': [
      'What is a MatrixOne data branch?',
      'How does MatrixOne implement HTAP?'
    ],
    '/getting-started/': [
      'Can I run MatrixOne with Docker?',
      'How do I connect with a MySQL client?',
      "What's the default password and how do I change it?"
    ],
    '/overview/': [
      'How is MatrixOne different from MySQL?',
      'What scenarios does MatrixOne fit?',
      'How does multi-tenancy work?'
    ],
    '/release-notes/': [
      "What's new in the latest release?",
      'Are there breaking changes from v23 to v25?'
    ],
    '/faqs/': [
      'Does MatrixOne support the MySQL protocol?',
      'Which version is recommended for production?',
      'Is there a cloud version?'
    ],
    '/develop/': [
      'How do I import bulk data?',
      'What ORMs are supported?'
    ],
    '/deploy/': [
      'How do I deploy on Kubernetes?',
      'What are the minimum cluster specs?'
    ],
    'default': [
      'What is MatrixOne?',
      'How is MatrixOne different from MySQL?',
      'How do I get started quickly?'
    ]
  } : {
    '/sql-reference/snapshot': [
      '如何为单表创建快照？',
      '快照和数据分支有什么区别？',
      '基于快照恢复会覆盖现有数据吗？'
    ],
    '/sql-reference/': [
      'CREATE SNAPSHOT 怎么用？',
      'MatrixOne 支持 MERGE INTO 吗？',
      'EXPLAIN 输出格式和 MySQL 有什么不同？'
    ],
    '/concepts/data-branch': [
      '数据分支和 Git 分支一样吗？',
      '一个分支会占多少存储？',
      '分支合并冲突怎么处理？'
    ],
    '/concepts/': [
      '什么是 MatrixOne 数据分支？',
      'MatrixOne 怎么实现 HTAP？'
    ],
    '/getting-started/': [
      '能不能用 Docker 启动？',
      '怎么用 MySQL 客户端连接？',
      '默认密码是什么？怎么改？'
    ],
    '/overview/': [
      'MatrixOne 和 MySQL 有什么区别？',
      'MatrixOne 适合哪些场景？',
      '怎么实现多租户隔离？'
    ],
    '/release-notes/': [
      '最新版本有什么新功能？',
      '从 v23 升级到 v25 有不兼容吗？'
    ],
    '/faqs/': [
      'MatrixOne 支持 MySQL 协议吗？',
      '生产环境推荐哪个版本？',
      '有云版本吗？'
    ],
    '/develop/': [
      '怎么批量导入数据？',
      '支持哪些 ORM 框架？'
    ],
    '/deploy/': [
      '怎么部署到 Kubernetes？',
      '集群最小硬件要求？'
    ],
    'default': [
      '什么是 MatrixOne？',
      'MatrixOne 和 MySQL 有什么区别？',
      '怎么快速上手 MatrixOne？'
    ]
  };

  function pickSuggestions() {
    var path = location.pathname;
    var keys = Object.keys(PAGE_SUGGESTIONS);
    /* 按 key 长度降序，先匹配更精确的路径 */
    keys.sort(function (a, b) { return b.length - a.length; });
    for (var i = 0; i < keys.length; i++) {
      if (keys[i] !== 'default' && path.indexOf(keys[i]) !== -1) {
        return PAGE_SUGGESTIONS[keys[i]];
      }
    }
    return PAGE_SUGGESTIONS['default'];
  }

  /* =========================================================
     2. 演示场景（关键词→丰富回答）
     ========================================================= */
  var DEMO_RESPONSES = LANG === 'en' ? [
    {
      keywords: ['branch', 'merge', 'promo', 'data version', '数据版本'],
      content:
'**Data Branch** is MatrixOne\'s lightweight data version-management capability. Use it for promo campaigns, A/B testing, or as a safety net before risky operations.\n\n' +
'**Full workflow example**:\n\n' +
'```sql\n' +
'-- 1. Create a new branch from master\n' +
'CREATE BRANCH promo_2025 FROM master;\n' +
'```\n\n' +
'```sql\n' +
'-- 2. Switch to the branch and prepare promo data\n' +
'USE BRANCH promo_2025;\n' +
'INSERT INTO orders (customer_id, amount, promo_code)\n' +
'SELECT customer_id, amount * 0.85, \'SUMMER25\'\n' +
'FROM orders WHERE category = \'electronics\';\n' +
'```\n\n' +
'```sql\n' +
'-- 3. Merge back to master after validation\n' +
'MERGE INTO master FROM promo_2025\n' +
'WHEN CONFLICT THEN PREFER promo_2025;\n' +
'```\n\n' +
'```sql\n' +
'-- 4. Or discard the branch if something is off\n' +
'DROP BRANCH promo_2025;\n' +
'```\n\n' +
'Branch creation is **O(1)** (millisecond-level, no data copy). Merging applies deltas through MVCC.',
      sources: [
        { label: 'Data Branch concepts', url: '/en/concepts/data-branch.html' },
        { label: 'MERGE INTO syntax', url: '#' },
        { label: 'Conflict resolution policies', url: '#' }
      ],
      followups: [
        'How do I check storage usage of a branch?',
        'Is there an auto-merge strategy for conflicts?'
      ]
    },
    {
      keywords: ['snapshot', '快照'],
      content:
'`CREATE SNAPSHOT` creates a **read-only** point-in-time snapshot for backup, audit, or time-travel queries.\n\n' +
'**Basic usage**:\n\n' +
'```sql\n' +
'CREATE SNAPSHOT snap_demo_20260424\n' +
'  FOR DATABASE demo\n' +
'  COMMENT \'pre-release snapshot\';\n' +
'```\n\n' +
'**Restoring from a snapshot**:\n\n' +
'```sql\n' +
'RESTORE DATABASE demo FROM SNAPSHOT snap_demo_20260424;\n' +
'```\n\n' +
'Snapshots are **O(1)** to create, with near-zero storage cost (metadata only).\n' +
'Difference from data branches: snapshots are read-only and used for backup; branches are writable and used for parallel dev.',
      sources: [
        { label: 'CREATE SNAPSHOT syntax', url: '/en/sql-reference/snapshot.html' },
        { label: 'Backup & restore', url: '#' }
      ],
      followups: [
        'Can a snapshot be restored across clusters?',
        'How do I combine PITR with snapshots?'
      ]
    },
    {
      keywords: ['mysql', 'compat', 'protocol', '兼容'],
      content:
'MatrixOne is highly compatible with the **MySQL 8.0 wire protocol** — most MySQL clients and drivers connect out of the box.\n\n' +
'**Supported**:\n' +
'- Most DDL / DML / DCL\n' +
'- Common functions and operators\n' +
'- JDBC / pymysql / go-sql-driver\n' +
'- Tools: Navicat / DBeaver / MySQL Workbench\n\n' +
'**Not supported**:\n' +
'- `CREATE TRIGGER` / `CREATE PROCEDURE`\n' +
'- MySQL native full-text search (replaced by vector search)\n' +
'- GIS spatial indexes\n\n' +
'**MatrixOne extensions** (no MySQL equivalent): `SNAPSHOT`, `BRANCH`, `PITR`.\n\n' +
'Migration tip: < 100GB use `mo-dump`; larger use DataX or FlinkCDC.',
      sources: [
        { label: 'MySQL compatibility detail', url: '/en/overview/feature/mysql-compatibility.html' },
        { label: 'Migration tools comparison', url: '#' },
        { label: 'MatrixOne vs TiDB / Aurora', url: '/en/overview/matrixone-vs-other_databases/matrixone-vs-oltp.html' }
      ],
      followups: [
        'Which MySQL clients work?',
        'How do I migrate from MySQL to MatrixOne?'
      ]
    }
  ] : [
    {
      keywords: ['分支', '合并', '促销', '数据版本', 'branch', 'merge'],
      content:
'**数据分支（Data Branch）** 是 MatrixOne 提供的轻量级数据版本管理能力。典型场景：促销活动数据预备、A/B 测试、风险操作前的安全绳。\n\n' +
'**完整工作流示例**：\n\n' +
'```sql\n' +
'-- 1. 从主干创建一个新分支\n' +
'CREATE BRANCH promo_2025 FROM master;\n' +
'```\n\n' +
'```sql\n' +
'-- 2. 切到分支后做促销数据预备\n' +
'USE BRANCH promo_2025;\n' +
'INSERT INTO orders (customer_id, amount, promo_code)\n' +
'SELECT customer_id, amount * 0.85, \'SUMMER25\'\n' +
'FROM orders WHERE category = \'electronics\';\n' +
'```\n\n' +
'```sql\n' +
'-- 3. 验证数据无误后，合并回主干\n' +
'MERGE INTO master FROM promo_2025\n' +
'WHEN CONFLICT THEN PREFER promo_2025;\n' +
'```\n\n' +
'```sql\n' +
'-- 4. 或者直接丢弃分支不合并\n' +
'DROP BRANCH promo_2025;\n' +
'```\n\n' +
'数据分支是 **O(1) 创建**（毫秒级，不复制数据），合并通过 MVCC 增量应用。',
      sources: [
        { label: '数据分支介绍', url: '/zh/concepts/data-branch.html' },
        { label: 'MERGE INTO 命令', url: '#' },
        { label: '冲突策略', url: '#' }
      ],
      followups: [
        '如何看一个分支占用多少存储？',
        '有没有自动合并冲突的策略？'
      ]
    },
    {
      keywords: ['快照', 'snapshot'],
      content:
'`CREATE SNAPSHOT` 用于为数据库或表创建**只读**时间点快照，适用于备份、审计、时间旅行查询。\n\n' +
'**基础用法**：\n\n' +
'```sql\n' +
'CREATE SNAPSHOT snap_demo_20260424\n' +
'  FOR DATABASE demo\n' +
'  COMMENT \'上线前快照\';\n' +
'```\n\n' +
'**基于快照恢复**：\n\n' +
'```sql\n' +
'RESTORE DATABASE demo FROM SNAPSHOT snap_demo_20260424;\n' +
'```\n\n' +
'快照创建是 **O(1)** 操作，几乎零存储开销（只记录元数据）。\n' +
'和数据分支的区别：快照只读、用于备份；分支可读写、用于并行开发。',
      sources: [
        { label: 'CREATE SNAPSHOT 语法', url: '/zh/sql-reference/snapshot.html' },
        { label: '备份与恢复', url: '#' }
      ],
      followups: [
        '快照能跨集群恢复吗？',
        'PITR 和快照怎么搭配？'
      ]
    },
    {
      keywords: ['mysql', '兼容', 'protocol', '协议'],
      content:
'MatrixOne 高度兼容 **MySQL 8.0 协议**，绝大多数 MySQL 客户端和驱动可以直接连接。\n\n' +
'**支持**：\n' +
'- 大部分 DDL / DML / DCL 语法\n' +
'- 大部分函数和操作符\n' +
'- JDBC / pymysql / go-sql-driver\n' +
'- 工具：Navicat / DBeaver / MySQL Workbench\n\n' +
'**不支持**：\n' +
'- `CREATE TRIGGER` / `CREATE PROCEDURE`（触发器和存储过程）\n' +
'- MySQL 原生全文检索（用自研向量检索替代）\n' +
'- GIS 空间索引\n\n' +
'**MatrixOne 独有**：`SNAPSHOT` / `BRANCH` / `PITR`，MySQL 没有。\n\n' +
'迁移建议：< 100 GB 用 `mo-dump`；超过用 DataX 或 FlinkCDC 增量同步。',
      sources: [
        { label: 'MySQL 兼容性详解', url: '/zh/overview/feature/mysql-compatibility.html' },
        { label: '数据迁移工具对比', url: '#' },
        { label: '与 TiDB / Aurora 对比', url: '/zh/overview/matrixone-vs-other_databases/matrixone-vs-oltp.html' }
      ],
      followups: [
        '支持哪些 MySQL 客户端？',
        '怎么从 MySQL 迁移到 MatrixOne？'
      ]
    }
  ];

  var DEFAULT_RESPONSE = LANG === 'en' ? {
    content: '> This is the demo version of the docs assistant — only a few preset questions are answerable right now. The full version will be backed by a RAG service that can answer anything about MatrixOne.\n\nTry the suggestions above for a richer demo flow.',
    sources: [],
    followups: []
  } : {
    content: '> 这是演示版的文档助手，当前只能回答部分预置问题。完整版将接入 RAG 服务，能回答任何关于 MatrixOne 的问题。\n\n试试上方的推荐问题查看完整演示效果。',
    sources: [],
    followups: []
  };

  function matchScenario(question) {
    var lower = question.toLowerCase();
    for (var i = 0; i < DEMO_RESPONSES.length; i++) {
      var r = DEMO_RESPONSES[i];
      for (var j = 0; j < r.keywords.length; j++) {
        if (lower.indexOf(r.keywords[j].toLowerCase()) !== -1) return r;
      }
    }
    return DEFAULT_RESPONSE;
  }

  /* =========================================================
     3. 极简 Markdown 渲染（fence + 行内 code + bold + 引用）
     ========================================================= */
  function escapeHtml(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function renderMarkdown(text) {
    var html = '';
    var re = /```(\w*)\n([\s\S]*?)```/g;
    var lastIndex = 0;
    var m;
    while ((m = re.exec(text)) !== null) {
      html += renderInline(text.slice(lastIndex, m.index));
      html += renderCode(m[2], m[1]);
      lastIndex = re.lastIndex;
    }
    html += renderInline(text.slice(lastIndex));
    return html;
  }
  function renderInline(text) {
    if (!text || !text.trim()) return '';
    return text.split(/\n\n+/).map(function (p) {
      var trimmed = p.trim();
      if (!trimmed) return '';
      var isQuote = trimmed.indexOf('> ') === 0;
      if (isQuote) trimmed = trimmed.replace(/^> /gm, '');
      /* 列表 */
      if (/^[-*]\s/.test(trimmed)) {
        var items = trimmed.split('\n').map(function (line) {
          var li = line.replace(/^[-*]\s/, '');
          return '<li>' + applyInline(escapeHtml(li)) + '</li>';
        }).join('');
        return '<ul>' + items + '</ul>';
      }
      var html = applyInline(escapeHtml(trimmed)).replace(/\n/g, '<br>');
      return isQuote ? '<blockquote>' + html + '</blockquote>' : '<p>' + html + '</p>';
    }).join('');
  }
  function applyInline(html) {
    /* 注意：在 escape 之后操作 */
    html = html.replace(/\*\*([^*\n]+)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/`([^`\n]+)`/g, '<code>$1</code>');
    return html;
  }
  function renderCode(code, lang) {
    var escaped = escapeHtml(code.replace(/\n+$/, ''));
    if (/^(sql|mysql)$/i.test(lang)) escaped = highlightSQL(escaped);
    else if (/^(bash|sh|zsh|shell)$/i.test(lang)) escaped = highlightBash(escaped);
    return '<pre class="mo-msg-code"><code>' + escaped + '</code></pre>';
  }
  /* 简易 SQL 着色（同正文 .k / .s / .m / .c / .mo-keyword 类） */
  var SQL_RE = /(--[^\n]*)|('(?:[^'\\]|\\.)*'|"[^"\n]*")|\b(\d+(?:\.\d+)?)\b|\b(SNAPSHOT|SNAPSHOTS|BRANCH|BRANCHES|PITR|RESTORE|CLONE|VECF32|VECF64|CDC|HTAP|HSTAP|DATABRANCH|DATA\s+BRANCH|MERGE\s+INTO|WHEN\s+CONFLICT|FOR\s+SYSTEM_TIME|CREATE\s+SNAPSHOT|DROP\s+SNAPSHOT|CREATE\s+BRANCH|DROP\s+BRANCH|USE\s+BRANCH)\b|\b(SELECT|FROM|WHERE|JOIN|LEFT|RIGHT|INNER|OUTER|FULL|CROSS|ON|AS|AND|OR|NOT|IN|IS|NULL|CREATE|DROP|ALTER|TABLE|DATABASE|VIEW|INDEX|INSERT|INTO|VALUES|UPDATE|SET|DELETE|MERGE|WHEN|MATCHED|THEN|TRUNCATE|GROUP|BY|ORDER|LIMIT|OFFSET|HAVING|UNION|ALL|EXCEPT|INTERSECT|FOR|WITH|CASE|END|BEGIN|COMMIT|ROLLBACK|TRANSACTION|USE|SHOW|EXPLAIN|IF|EXISTS|PRIMARY|KEY|FOREIGN|UNIQUE|CONSTRAINT|REFERENCES|DEFAULT|VARCHAR|INT|BIGINT|TIMESTAMP|TEXT|BOOL|DECIMAL|DOUBLE|FLOAT|DATE|DATETIME|JSON|PREFER)\b/gi;
  function highlightSQL(escaped) {
    return escaped.replace(SQL_RE, function (m, c, s, n, dialect, kw) {
      if (c) return '<span class="c">' + m + '</span>';
      if (s) return '<span class="s">' + m + '</span>';
      if (n) return '<span class="m">' + m + '</span>';
      if (dialect) return '<span class="mo-keyword">' + m + '</span>';
      if (kw) return '<span class="k">' + m + '</span>';
      return m;
    });
  }
  var BASH_RE = /(#[^\n]*)|('[^'\n]*'|"[^"\n]*")|(\$[A-Za-z_][A-Za-z0-9_]*)|\b(echo|export|cd|ls|mkdir|rm|cp|mv|cat|grep|sed|awk|find|chmod|chown|sudo|apt|yum|brew|docker|git|make|npm|pnpm|yarn|cargo|go|python|mysql|curl|wget|ssh|scp|tar|unzip)\b/g;
  function highlightBash(escaped) {
    return escaped.replace(BASH_RE, function (m, c, s, v, kw) {
      if (c) return '<span class="c">' + m + '</span>';
      if (s) return '<span class="s">' + m + '</span>';
      if (v) return '<span class="nv">' + m + '</span>';
      if (kw) return '<span class="k">' + m + '</span>';
      return m;
    });
  }

  /* =========================================================
     4. SVG 资源
     ========================================================= */
  var SPARKLES_BIG =
    '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">' +
      '<path d="M12 2l1.8 6.2L20 10l-6.2 1.8L12 18l-1.8-6.2L4 10l6.2-1.8L12 2z"/>' +
      '<path d="M19 13l.9 2.1L22 16l-2.1.9L19 19l-.9-2.1L16 16l2.1-.9L19 13z"/>' +
      '<path d="M5 14l.7 1.8L7.5 16.5l-1.8.7L5 19l-.7-1.8L2.5 16.5l1.8-.7L5 14z"/>' +
    '</svg>';
  var SPARKLES_SMALL =
    '<svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">' +
      '<path d="M8 1l1.2 4.1L13.5 6.5 9.2 7.8 8 12 6.8 7.8 2.5 6.5 6.8 5.1 8 1z"/>' +
    '</svg>';
  var PLUS_ICON =
    '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">' +
      '<path d="M8 3v10M3 8h10" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>' +
    '</svg>';
  var SEND_ICON =
    '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">' +
      '<path d="M2 13L14 8L2 3v4l8 1-8 1v4z" fill="currentColor"/>' +
    '</svg>';
  var CLOSE_ICON =
    '<svg viewBox="0 0 16 16" fill="none" aria-hidden="true">' +
      '<path d="M3 3l10 10M13 3L3 13" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>' +
    '</svg>';

  /* =========================================================
     5. 状态 & DOM 引用
     ========================================================= */
  var fab, overlay, drawer, body, msgsEl, welcomeEl, suggestEl, formEl, inputEl, sendBtn, counterEl, plusBtn;
  var hasInteracted = false;
  var thinkingEl = null;

  /* =========================================================
     6. 构建 DOM
     ========================================================= */
  function build() {
    fab = document.createElement('button');
    fab.className = 'mo-fab';
    fab.setAttribute('aria-label', T.openLabel);
    fab.setAttribute('type', 'button');
    fab.innerHTML = SPARKLES_BIG;

    overlay = document.createElement('div');
    overlay.className = 'mo-overlay';

    drawer = document.createElement('aside');
    drawer.className = 'mo-drawer';
    drawer.setAttribute('aria-hidden', 'true');
    drawer.innerHTML =
      '<div class="mo-drawer__header">' +
        '<div class="mo-drawer__brand">' +
          '<span class="mo-drawer__brand-icon">' + SPARKLES_SMALL + '</span>' +
          '<span>' + T.brand + '</span>' +
        '</div>' +
        '<button class="mo-drawer__close" type="button" aria-label="' + T.closeLabel + '">' + CLOSE_ICON + '</button>' +
      '</div>' +
      '<div class="mo-drawer__body">' +
        '<div class="mo-drawer__welcome">' +
          '<div class="mo-drawer__welcome-icon">' + SPARKLES_BIG + '</div>' +
          '<h3>' + T.welcomeTitle + '</h3>' +
          '<p>' + T.welcomeSubtitle + '</p>' +
        '</div>' +
        '<div class="mo-drawer__suggestions">' +
          '<div class="mo-drawer__sug-head">' + T.suggestionHead + '</div>' +
          '<div class="mo-drawer__sug-list"></div>' +
        '</div>' +
        '<div class="mo-drawer__messages"></div>' +
      '</div>' +
      '<form class="mo-drawer__input">' +
        '<div class="mo-drawer__counter"><span class="mo-drawer__counter-num">0</span> / 500</div>' +
        '<div class="mo-drawer__input-row">' +
          '<button type="button" class="mo-drawer__plus" tabindex="-1" aria-label="' + T.attachLabel + '">' + PLUS_ICON + '</button>' +
          '<textarea rows="1" maxlength="500" placeholder="' + T.placeholder + '"></textarea>' +
          '<button type="submit" class="mo-drawer__send" disabled aria-label="' + T.sendLabel + '">' + SEND_ICON + '</button>' +
        '</div>' +
      '</form>';

    document.body.appendChild(fab);
    document.body.appendChild(overlay);
    document.body.appendChild(drawer);

    /* refs */
    body = drawer.querySelector('.mo-drawer__body');
    msgsEl = drawer.querySelector('.mo-drawer__messages');
    welcomeEl = drawer.querySelector('.mo-drawer__welcome');
    suggestEl = drawer.querySelector('.mo-drawer__suggestions');
    formEl = drawer.querySelector('.mo-drawer__input');
    inputEl = drawer.querySelector('textarea');
    sendBtn = drawer.querySelector('.mo-drawer__send');
    counterEl = drawer.querySelector('.mo-drawer__counter-num');
    plusBtn = drawer.querySelector('.mo-drawer__plus');

    renderSuggestions();
    wireEvents();
  }

  function renderSuggestions() {
    var sugs = pickSuggestions();
    var listEl = drawer.querySelector('.mo-drawer__sug-list');
    listEl.innerHTML = sugs.map(function (s) {
      return '<button type="button" class="mo-drawer__sug">' + escapeHtml(s) + '</button>';
    }).join('');
    listEl.querySelectorAll('.mo-drawer__sug').forEach(function (b) {
      b.addEventListener('click', function () { submit(b.textContent); });
    });
  }

  function wireEvents() {
    fab.addEventListener('click', open);
    overlay.addEventListener('click', close);
    drawer.querySelector('.mo-drawer__close').addEventListener('click', close);
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.classList.contains('is-open')) close();
    });

    inputEl.addEventListener('input', updateInputUI);
    inputEl.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        if (!sendBtn.disabled) formEl.dispatchEvent(new Event('submit', { cancelable: true }));
      }
    });
    formEl.addEventListener('submit', function (e) {
      e.preventDefault();
      var q = inputEl.value.trim();
      if (!q) return;
      submit(q);
      inputEl.value = '';
      updateInputUI();
    });

    plusBtn.addEventListener('click', function () {
      showToast(T.attachLabel);
    });
  }

  function open() {
    drawer.classList.add('is-open');
    overlay.classList.add('is-open');
    drawer.setAttribute('aria-hidden', 'false');
    setTimeout(function () { inputEl.focus(); }, 280);
  }
  function close() {
    drawer.classList.remove('is-open');
    overlay.classList.remove('is-open');
    drawer.setAttribute('aria-hidden', 'true');
  }

  function updateInputUI() {
    var len = inputEl.value.length;
    counterEl.textContent = len;
    counterEl.parentElement.classList.toggle('is-warn', len > 450);
    sendBtn.disabled = !inputEl.value.trim();
    inputEl.style.height = 'auto';
    inputEl.style.height = Math.min(inputEl.scrollHeight, 96) + 'px';
  }

  /* =========================================================
     7. 消息流
     ========================================================= */
  function submit(text) {
    if (!hasInteracted) {
      hasInteracted = true;
      drawer.classList.add('mo-drawer--interacted');
    }
    addUserMsg(text);
    showThinking();
    setTimeout(function () {
      hideThinking();
      var resp = matchScenario(text);
      addBotMsg(resp);
    }, 600);
  }

  function addUserMsg(text) {
    var m = document.createElement('div');
    m.className = 'mo-msg mo-msg--user';
    m.textContent = text;
    msgsEl.appendChild(m);
    scrollToBottom();
  }

  function showThinking() {
    thinkingEl = document.createElement('div');
    thinkingEl.className = 'mo-msg mo-msg--bot mo-msg--thinking';
    thinkingEl.innerHTML = '<span></span><span></span><span></span>';
    msgsEl.appendChild(thinkingEl);
    scrollToBottom();
  }
  function hideThinking() {
    if (thinkingEl) { thinkingEl.remove(); thinkingEl = null; }
  }

  function addBotMsg(resp) {
    var m = document.createElement('div');
    m.className = 'mo-msg mo-msg--bot';
    m.innerHTML =
      '<div class="mo-msg__head">' + SPARKLES_SMALL + '<span>' + T.brand + '</span></div>' +
      '<div class="mo-msg__body"></div>' +
      '<div class="mo-msg__sources" hidden></div>' +
      '<div class="mo-msg__followups" hidden></div>' +
      '<div class="mo-msg__feedback" hidden>' +
        '<button type="button" class="mo-msg__fb mo-msg__fb--up" aria-label="helpful">👍</button>' +
        '<button type="button" class="mo-msg__fb mo-msg__fb--down" aria-label="not helpful">👎</button>' +
      '</div>';
    msgsEl.appendChild(m);

    var bodyEl = m.querySelector('.mo-msg__body');
    var fullHtml = renderMarkdown(resp.content || '');
    streamInto(bodyEl, fullHtml, function () {
      revealExtras(m, resp);
    });
  }

  /* 流式展示：先以 textContent 一字字打出，结束后整体替换为渲染好的 HTML */
  function streamInto(targetEl, fullHtml, onDone) {
    var temp = document.createElement('div');
    temp.innerHTML = fullHtml;
    var plain = (temp.textContent || temp.innerText || '').replace(/\n+/g, '\n');
    var i = 0;
    var step = 2;
    var speed = 25;
    var timer = setInterval(function () {
      i += step;
      if (i >= plain.length) {
        clearInterval(timer);
        targetEl.innerHTML = fullHtml;
        scrollToBottom();
        if (onDone) onDone();
      } else {
        targetEl.textContent = plain.slice(0, i);
        scrollToBottom();
      }
    }, speed);
  }

  function revealExtras(m, resp) {
    /* sources */
    if (resp.sources && resp.sources.length) {
      var s = m.querySelector('.mo-msg__sources');
      s.innerHTML =
        '<div class="mo-msg__extras-head">' + T.sourceHead + '</div>' +
        resp.sources.map(function (src) {
          return '<a class="mo-msg__source" href="' + (src.url || '#') + '" target="_blank" rel="noopener">' +
                 escapeHtml(src.label) + '</a>';
        }).join('');
      s.hidden = false;
    }
    /* followups */
    if (resp.followups && resp.followups.length) {
      var f = m.querySelector('.mo-msg__followups');
      f.innerHTML =
        '<div class="mo-msg__extras-head">' + T.followupHead + '</div>' +
        resp.followups.map(function (q) {
          return '<button type="button" class="mo-msg__fu">' + escapeHtml(q) + '</button>';
        }).join('');
      f.hidden = false;
      f.querySelectorAll('.mo-msg__fu').forEach(function (b) {
        b.addEventListener('click', function () { submit(b.textContent); });
      });
    }
    /* feedback */
    var fb = m.querySelector('.mo-msg__feedback');
    fb.hidden = false;
    fb.querySelectorAll('.mo-msg__fb').forEach(function (btn) {
      btn.addEventListener('click', function () {
        fb.querySelectorAll('.mo-msg__fb').forEach(function (b) { b.classList.remove('is-active'); });
        btn.classList.add('is-active');
        showToast(T.feedbackThanks);
      });
    });
    scrollToBottom();
  }

  function scrollToBottom() {
    body.scrollTop = body.scrollHeight;
  }

  /* =========================================================
     8. Toast
     ========================================================= */
  function showToast(text) {
    var t = document.createElement('div');
    t.className = 'mo-toast';
    t.textContent = text;
    document.body.appendChild(t);
    requestAnimationFrame(function () { t.classList.add('is-visible'); });
    setTimeout(function () {
      t.classList.remove('is-visible');
      setTimeout(function () { t.remove(); }, 300);
    }, 1500);
  }

  /* =========================================================
     9. 启动
     ========================================================= */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
