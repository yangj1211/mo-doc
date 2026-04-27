/* 固定顶栏（Snowflake 风格）—— Logo + 字标 + 搜索 + 语言 pill + 暗色 + 分类 Tab
   - 挂载到 body 顶部；Furo 侧边栏和正文通过 CSS 下移
   - 相对路径在 lang 前缀（/zh/ 或 /en/）下解析，切换语言后依然正确 */
(function () {
  'use strict';
  if (document.querySelector('.mo-topbar')) return;

  var LANG = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0 ? 'en' : 'zh';
  var I18N = {
    zh: {
      docsLabel: '文档',
      searchPlaceholder: '搜索文档...',
      tabs: [
        { label: '快速开始',  path: 'getting-started/quickstart.html', match: 'getting-started' },
        { label: '产品概述',  path: 'overview/index.html',             match: 'overview' },
        { label: '开发指南',  path: 'develop/index.html',              match: 'develop' },
        { label: 'SQL 参考',  path: 'sql-reference/index.html',     match: 'sql-reference' },
        { label: '常见问题',  path: 'faqs/index.html',                 match: 'faqs' },
        { label: '版本发布',  path: 'release-notes/index.html',        match: 'release-notes' }
      ]
    },
    en: {
      docsLabel: 'Docs',
      searchPlaceholder: 'Search docs...',
      tabs: [
        { label: 'Quickstart',     path: 'getting-started/quickstart.html', match: 'getting-started' },
        { label: 'Overview',       path: 'overview/index.html',             match: 'overview' },
        { label: 'Develop',        path: 'develop/index.html',              match: 'develop' },
        { label: 'SQL Reference',  path: 'sql-reference/index.html',     match: 'sql-reference' },
        { label: 'FAQ',            path: 'faqs/index.html',                 match: 'faqs' },
        { label: 'Release Notes',  path: 'release-notes/index.html',        match: 'release-notes' }
      ]
    }
  };
  var T = I18N[LANG];

  function langPrefix() {
    /* URL 形如 /<product>/<lang>/...；返回 "/<product>/<lang>/" */
    var m = location.pathname.match(/^(\/[a-z][a-z0-9-]+\/(?:zh|en))(?:\/|$)/);
    return m ? m[1] + '/' : '/' + LANG + '/';
  }

  function currentSection() {
    var prefix = langPrefix();
    var rest = location.pathname.indexOf(prefix) === 0
      ? location.pathname.slice(prefix.length)
      : location.pathname;
    return (rest.split('/')[0] || '').toLowerCase();
  }

  // 官方 MatrixOrigin lockup（MO 笑脸图标 + Matrix Origin 字标）
  // 明暗两套 PNG-in-SVG，由 CSS 切换显隐
  function logoHtml(prefix) {
    return (
      '<img src="' + prefix + '_static/images/matrixone-logo-light.svg" ' +
           'class="mo-topbar__logo mo-topbar__logo--light" alt="MatrixOrigin" />' +
      '<img src="' + prefix + '_static/images/matrixone-logo-dark.svg" ' +
           'class="mo-topbar__logo mo-topbar__logo--dark" alt="MatrixOrigin" />'
    );
  }
  var SEARCH_ICON =
    '<svg viewBox="0 0 24 24" class="mo-topbar__search-icon" aria-hidden="true">' +
      '<path fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"' +
      ' d="M10.5 3a7.5 7.5 0 0 1 5.93 12.07l4.25 4.26M10.5 18A7.5 7.5 0 1 1 10.5 3"/>' +
    '</svg>';

  function build() {
    var prefix = langPrefix();
    var cur = currentSection();

    var tabsHtml = T.tabs.map(function (t) {
      var active = t.match === cur ? ' mo-topbar__tab--active' : '';
      return '<a class="mo-topbar__tab' + active + '" href="' + prefix + t.path + '">' +
             t.label + '</a>';
    }).join('');

    var bar = document.createElement('header');
    bar.className = 'mo-topbar';
    bar.innerHTML =
      '<div class="mo-topbar__inner">' +
        /* 1. Brand */
        '<a class="mo-topbar__brand" href="' + prefix + '" aria-label="MatrixOrigin Docs">' +
          logoHtml(prefix) +
          '<span class="mo-topbar__docs">' + T.docsLabel + '</span>' +
        '</a>' +
        /* 2. Main nav */
        '<nav class="mo-topbar__tabs" aria-label="sections">' + tabsHtml + '</nav>' +
        /* 3. Tools (search + theme toggle + lang pill) —— 通过 margin-left:auto 推到右边 */
        '<div class="mo-topbar__tools">' +
          '<form class="mo-topbar__search" role="search">' +
            SEARCH_ICON +
            '<input type="search" autocomplete="off" placeholder="' + T.searchPlaceholder + '" />' +
            '<kbd>/</kbd>' +
          '</form>' +
          '<div class="mo-topbar__actions"></div>' +
        '</div>' +
      '</div>';

    document.body.insertBefore(bar, document.body.firstChild);
    document.body.classList.add('mo-has-topbar');

    // 把 Furo 的桌面端暗色切换按钮搬进 topbar actions（移动端那个保留原位）
    var actions = bar.querySelector('.mo-topbar__actions');
    var themeToggle = document.querySelector('.theme-toggle-container.theme-toggle-content');
    if (themeToggle) actions.appendChild(themeToggle);

    // 搜索：回车跳到 /{lang}/search.html?q=...
    var form = bar.querySelector('.mo-topbar__search');
    var input = form.querySelector('input');
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var q = input.value.trim();
      if (!q) return;
      location.href = prefix + 'search.html?q=' + encodeURIComponent(q);
    });

    // "/" 全局快捷键聚焦搜索
    document.addEventListener('keydown', function (e) {
      if (e.key !== '/') return;
      var tag = e.target.tagName;
      if (tag === 'INPUT' || tag === 'TEXTAREA' || e.target.isContentEditable) return;
      e.preventDefault();
      input.focus();
    });

  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
