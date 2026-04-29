/* 语言切换 pill —— 注入到 Furo 的 .theme-toggle-container
   （桌面端在文章右上角、移动端在顶部导航，和暗色模式按钮相邻）
   - URL 形如 /<product>/<lang>/...，识别后保留 product，只翻 lang
   - 当目标语言不存在（HAS_EN 不含当前 product 且当前是 zh）时不渲染 pill
   - 保留剩余路径、查询串和 hash */
(function () {
  'use strict';

  var LABEL = { zh: 'EN', en: '中文' };
  var TITLE = { zh: '切换到 English', en: 'Switch to 中文' };

  /* 产品的英文覆盖度：
     - HAS_EN：英文站完整覆盖中文，所有页面都能切（matrixone）
     - PARTIAL_EN：英文站只翻了少量页面，列出 rest 路径白名单，
       不在表里的中文页 zh→en pill 不显示，避免点出 404。
       en→zh 永远显示（中文站是全集）。 */
  var HAS_EN = { matrixone: true };
  var PARTIAL_EN = {
    'matrixone-intelligence': [
      '',                                                  /* 主页 /matrixone-intelligence/zh/ */
      'index.html',
      /* 8 个 section index 全部翻译 */
      'get-started/index.html',
      'overview/index.html',
      'workspace/index.html',
      'develop/index.html',
      'billing/index.html',
      'reference/index.html',
      'help/index.html',
      'release-notes/index.html',
      /* Get Started */
      'get-started/quickstart.html',
      'get-started/workspace.html',
      'get-started/parse_demo.html',
      'get-started/vector.html',
      'get-started/ai_search.html',
      'get-started/cv_search.html',
      /* Overview */
      'overview/matrixone-intelligence-introduction.html',
      'overview/mone-introduction.html',
      'overview/mysql-compatibility.html',
      /* Billing(完整翻译)*/
      'billing/account-overview.html',
      'billing/adjust-policy.html',
      'billing/bill-detail.html',
      'billing/cancellation-policy.html',
      'billing/coupons-management.html',
      'billing/overdraft.html',
      'billing/recharge.html',
      'billing/renew.html',
      'billing/revenue-expenditure-details.html',
      'billing/price-detail/price-detail-serverless.html',
      'billing/price-detail/price-detail-standard.html',
      /* Develop */
      'develop/workflow-api/automic_api.html',
      /* Help */
      'help/faqs/FAQ-Product.html',
      'help/faqs/sql-faqs.html',
      'help/glossary.html',
      'help/tech-support.html',
      'help/legal/privacy-policy.html',
      'help/legal/service-level-agreement.html',
      'help/legal/terms-of-service.html'
    ]
  };

  /* 解析 location.pathname → { product, lang, rest }，
     rest 形如 "getting-started/quickstart.html"（不带前导斜杠）。
     不匹配（比如根目录）返回 null。 */
  function parsePath() {
    var m = location.pathname.match(/^\/([a-z][a-z0-9-]+)\/(zh|en)(\/.*)?$/);
    if (!m) return null;
    var rest = m[3] || '/';
    if (rest.charAt(0) === '/') rest = rest.slice(1);
    return { product: m[1], lang: m[2], rest: rest };
  }

  function targetUrl(parsed) {
    var other = parsed.lang === 'zh' ? 'en' : 'zh';
    return '/' + parsed.product + '/' + other + '/' + parsed.rest +
           location.search + location.hash;
  }

  function makePill(parsed) {
    var pill = document.createElement('a');
    pill.className = 'mo-lang-pill';
    pill.href = targetUrl(parsed);
    pill.textContent = LABEL[parsed.lang];
    pill.title = TITLE[parsed.lang];
    pill.setAttribute('aria-label', TITLE[parsed.lang]);
    return pill;
  }

  function shouldRender(parsed) {
    if (!parsed) return false;
    /* 当前是 en：所有产品的中文站都是全集，永远显示 */
    if (parsed.lang === 'en') return true;
    /* 当前是 zh：英文全覆盖产品始终显示 */
    if (HAS_EN[parsed.product]) return true;
    /* 部分翻译产品：只在白名单页面上显示 */
    var partial = PARTIAL_EN[parsed.product];
    if (!partial) return false;
    return partial.indexOf(parsed.rest) !== -1;
  }

  function mount() {
    if (document.querySelector('.mo-lang-pill')) return;
    var parsed = parsePath();
    if (!shouldRender(parsed)) return;

    var containers = document.querySelectorAll('.theme-toggle-container');
    if (containers.length) {
      containers.forEach(function (c) {
        var btn = c.querySelector('.theme-toggle');
        var pill = makePill(parsed);
        if (btn) c.insertBefore(pill, btn);
        else c.appendChild(pill);
      });
    } else {
      /* 兜底：容器不存在时放视口右上角 */
      var pill = makePill(parsed);
      pill.classList.add('mo-lang-pill--floating');
      document.body.appendChild(pill);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
})();
