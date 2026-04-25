/* 语言切换 pill —— 注入到 Furo 的 .theme-toggle-container
   （桌面端在文章右上角、移动端在顶部导航，和暗色模式按钮相邻）
   - 识别 /zh/ 和 /en/ 两个 URL 前缀
   - 点击时替换前缀，保留剩余路径、查询串和 hash */
(function () {
  'use strict';

  var LABEL = { zh: 'EN', en: '中文' };
  var TITLE = { zh: '切换到 English', en: 'Switch to 中文' };

  function currentLang() {
    var p = location.pathname;
    if (p.indexOf('/zh/') === 0) return 'zh';
    if (p.indexOf('/en/') === 0) return 'en';
    return (document.documentElement.lang || 'zh').toLowerCase().indexOf('en') === 0 ? 'en' : 'zh';
  }

  function targetUrl(cur) {
    var other = cur === 'zh' ? 'en' : 'zh';
    var p = location.pathname;
    if (p.indexOf('/zh/') === 0) return '/' + other + '/' + p.slice(4) + location.search + location.hash;
    if (p.indexOf('/en/') === 0) return '/' + other + '/' + p.slice(4) + location.search + location.hash;
    return '/' + other + '/';
  }

  function makePill(cur) {
    var pill = document.createElement('a');
    pill.className = 'mo-lang-pill';
    pill.href = targetUrl(cur);
    pill.textContent = LABEL[cur];
    pill.title = TITLE[cur];
    pill.setAttribute('aria-label', TITLE[cur]);
    return pill;
  }

  function mount() {
    if (document.querySelector('.mo-lang-pill')) return;
    var cur = currentLang();
    var containers = document.querySelectorAll('.theme-toggle-container');
    if (containers.length) {
      containers.forEach(function (c) {
        var btn = c.querySelector('.theme-toggle');
        var pill = makePill(cur);
        if (btn) c.insertBefore(pill, btn);
        else c.appendChild(pill);
      });
    } else {
      // 兜底：容器不存在时放视口右上角
      var pill = makePill(cur);
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
