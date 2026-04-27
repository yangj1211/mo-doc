#!/usr/bin/env python3
"""
生成根目录产品选择页 build/html/index.html。

设计：
  - 自包含 HTML（内联 CSS），不依赖 Sphinx 主题资源，简单稳定。
  - 两张产品卡片 / 大间距 / 渐变品牌色 / 暗色模式自适应。
  - 卡片点击进入 /matrixone/ 或 /intelligence/，由那一层 redirect 选语言。
  - 浏览器语言英文时把页面文案切到英文版（matrixone 卡片描述词同步）。

用法：
  python scripts/build_picker.py build/html/index.html
"""
import sys
from pathlib import Path

HTML = """<!doctype html>
<html lang="zh-CN" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>MatrixOne 文档中心</title>
<style>
  :root {
    --mo-blue:        #004af0;
    --mo-blue-soft:   #3b82f6;
    --mo-purple:      #8b5cf6;
    --mo-purple-soft: #a78bfa;
    --bg:             #ffffff;
    --bg-soft:        #f8fafc;
    --ink-900:        #0f172a;
    --ink-600:        #475569;
    --ink-400:        #94a3b8;
    --border:         #e2e8f0;
    --shadow:         0 8px 32px rgba(15, 23, 42, 0.06);
    --shadow-hover:   0 16px 48px rgba(15, 23, 42, 0.10);
  }
  html[data-theme="dark"] {
    --bg:           #0b1220;
    --bg-soft:      #131c2e;
    --ink-900:      #e5e7eb;
    --ink-600:      #94a3b8;
    --ink-400:      #64748b;
    --border:       #1e293b;
    --shadow:       0 8px 32px rgba(0, 0, 0, 0.4);
    --shadow-hover: 0 16px 48px rgba(0, 0, 0, 0.55);
  }
  @media (prefers-color-scheme: dark) {
    html:not([data-theme="light"]) {
      --bg:           #0b1220;
      --bg-soft:      #131c2e;
      --ink-900:      #e5e7eb;
      --ink-600:      #94a3b8;
      --ink-400:      #64748b;
      --border:       #1e293b;
      --shadow:       0 8px 32px rgba(0, 0, 0, 0.4);
      --shadow-hover: 0 16px 48px rgba(0, 0, 0, 0.55);
    }
  }
  * { box-sizing: border-box; }
  html, body {
    margin: 0; padding: 0;
    background: var(--bg);
    color: var(--ink-900);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
                 "Hiragino Sans GB", "Microsoft YaHei", sans-serif;
    -webkit-font-smoothing: antialiased;
  }
  body {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 64px 24px;
  }
  .hero {
    text-align: center;
    margin-bottom: 56px;
    max-width: 720px;
  }
  .hero h1 {
    margin: 0 0 16px;
    font-size: clamp(2rem, 4vw, 2.8rem);
    font-weight: 700;
    letter-spacing: -.02em;
    background: linear-gradient(135deg, var(--mo-blue) 0%, var(--mo-purple) 100%);
    -webkit-background-clip: text; background-clip: text; color: transparent;
  }
  .hero p {
    margin: 0;
    font-size: 1.05rem;
    line-height: 1.6;
    color: var(--ink-600);
  }
  .cards {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
    width: 100%;
    max-width: 920px;
  }
  @media (max-width: 720px) {
    .cards { grid-template-columns: 1fr; }
  }
  .card {
    display: flex;
    flex-direction: column;
    background: var(--bg-soft);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 32px 28px 28px;
    text-decoration: none;
    color: inherit;
    box-shadow: var(--shadow);
    transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
    position: relative;
    overflow: hidden;
  }
  .card::before {
    content: '';
    position: absolute;
    inset: 0 0 auto 0;
    height: 4px;
    background: linear-gradient(90deg, var(--accent-from), var(--accent-to));
  }
  .card--mo  { --accent-from: var(--mo-blue);   --accent-to: var(--mo-blue-soft); }
  .card--moi { --accent-from: var(--mo-purple); --accent-to: var(--mo-purple-soft); }
  .card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-hover);
    border-color: var(--accent-from);
  }
  .card__title {
    font-size: 1.4rem;
    font-weight: 700;
    margin: 12px 0 8px;
    color: var(--ink-900);
    letter-spacing: -.01em;
  }
  .card__sub {
    font-size: .85rem;
    color: var(--accent-from);
    font-weight: 600;
    letter-spacing: .04em;
    text-transform: uppercase;
  }
  .card__desc {
    margin: 16px 0 24px;
    font-size: .98rem;
    line-height: 1.65;
    color: var(--ink-600);
    flex: 1;
  }
  .card__cta {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-size: .92rem;
    font-weight: 600;
    color: var(--accent-from);
  }
  .card__cta svg {
    width: 16px; height: 16px;
    transition: transform .18s ease;
  }
  .card:hover .card__cta svg { transform: translateX(3px); }
  .footer {
    margin-top: 56px;
    font-size: .85rem;
    color: var(--ink-400);
    text-align: center;
  }
  .footer a { color: inherit; text-decoration: none; border-bottom: 1px dashed var(--border); }
  .footer a:hover { color: var(--ink-600); }
</style>
</head>
<body>
  <main>
    <div class="hero">
      <h1 data-i18n="title">MatrixOne 文档中心</h1>
      <p  data-i18n="sub">选择你要查看的产品文档</p>
    </div>

    <div class="cards">
      <a class="card card--mo" href="/matrixone/">
        <span class="card__sub">数据库</span>
        <h2 class="card__title">MatrixOne</h2>
        <p class="card__desc" data-i18n="moDesc">
          面向 AI 时代的一体化数据库，在一套引擎中同时提供 OLTP、OLAP、流处理与向量检索能力。
        </p>
        <span class="card__cta">
          <span data-i18n="moCta">进入文档</span>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
               stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M5 12h14M13 5l7 7-7 7"/>
          </svg>
        </span>
      </a>

      <a class="card card--moi" href="/intelligence/">
        <span class="card__sub">AI 平台</span>
        <h2 class="card__title">MatrixOne Intelligence</h2>
        <p class="card__desc" data-i18n="moiDesc">
          一站式 DATA + AI 平台：GenAI 工作区、文档智能、Agent 构建，从数据到 AI 应用全链路。
        </p>
        <span class="card__cta">
          <span data-i18n="moiCta">进入文档</span>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
               stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
            <path d="M5 12h14M13 5l7 7-7 7"/>
          </svg>
        </span>
      </a>
    </div>

    <p class="footer" data-i18n="footer">
      由 Sphinx + Furo 构建。问题反馈请发送至
      <a href="mailto:docs@matrixorigin.cn">docs@matrixorigin.cn</a>。
    </p>
  </main>

<script>
  (function () {
    var EN = {
      title:   'MatrixOne Docs',
      sub:     'Choose the product to read',
      moDesc:  'An all-in-one database for the AI era — OLTP, OLAP, streaming, and vector search in a single engine.',
      moCta:   'Open docs',
      moiDesc: 'One-stop DATA + AI platform: GenAI workspaces, document intelligence, agent building — end-to-end from data to AI apps.',
      moiCta:  'Open docs',
      footer:  'Built with Sphinx + Furo. Send feedback to <a href="mailto:docs@matrixorigin.cn">docs@matrixorigin.cn</a>.'
    };
    var lang = (navigator.language || 'zh').toLowerCase();
    if (lang.indexOf('zh') !== 0) {
      document.documentElement.lang = 'en';
      Object.keys(EN).forEach(function (k) {
        var el = document.querySelector('[data-i18n="' + k + '"]');
        if (el) {
          if (k === 'footer') el.innerHTML = EN[k];
          else el.textContent = EN[k];
        }
      });
    }
  })();
</script>
</body>
</html>
"""


def main():
    if len(sys.argv) != 2:
        print('usage: build_picker.py <output.html>', file=sys.stderr)
        sys.exit(2)
    out = Path(sys.argv[1])
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(HTML, encoding='utf-8')
    print(f'  picker → {out}')


if __name__ == '__main__':
    main()
