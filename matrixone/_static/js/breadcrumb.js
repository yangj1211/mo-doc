/* 面包屑 + 更新时间
   - 面包屑数据来自 Furo 侧栏 .sidebar-tree li.current 链
   - 第一项是 home icon（点击回 lang 根）
   - 分隔符用 chevron
   - 下方一行 "最后更新于 <date>"，date 由 URL 哈希生成
     —— demo 环境无真 mtime，用确定性伪随机日期保证每次访问同一页
        看到的日期一致 */
(function () {
  'use strict';

  var LANG = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0 ? 'en' : 'zh';
  var T = LANG === 'en'
    ? { home: 'Home', updatedPrefix: 'Last updated on ' }
    : { home: '主页', updatedPrefix: '最后更新于 ' };

  var HOME_SVG =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2h-4v-7h-6v7H5a2 2 0 0 1-2-2z"/>' +
    '</svg>';
  var CHEVRON_SVG =
    '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<path d="M6 4l4 4-4 4"/>' +
    '</svg>';

  function langPrefix() {
    /* URL 形如 /<product>/<lang>/...；返回 "/<product>/<lang>/"。
       根目录（产品选择页）或非标准路径回退到 "/" */
    var m = location.pathname.match(/^(\/[a-z][a-z0-9-]+\/(?:zh|en))(?:\/|$)/);
    return m ? m[1] + '/' : '/';
  }

  function escapeHtml(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  /* 用 URL 路径生成确定性日期：同一页每次刷新都是同一个日期 */
  function fakeDate(path) {
    var hash = 0;
    for (var i = 0; i < path.length; i++) {
      hash = ((hash << 5) - hash) + path.charCodeAt(i);
      hash |= 0;
    }
    hash = Math.abs(hash);
    var now = new Date();
    var daysAgo = (hash % 200) + 1;            /* 过去 200 天内 */
    return new Date(now.getTime() - daysAgo * 86400000);
  }

  function formatDate(d) {
    if (LANG === 'en') {
      var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
      return months[d.getMonth()] + ' ' + d.getDate() + ', ' + d.getFullYear();
    }
    return d.getFullYear() + ' 年 ' + (d.getMonth() + 1) + ' 月 ' + d.getDate() + ' 日';
  }

  function build() {
    var article = document.querySelector('article[role="main"]');
    if (!article) return;
    if (article.querySelector('.mo-breadcrumb')) return;

    var currentLis = document.querySelectorAll('.sidebar-tree li.current');
    if (!currentLis.length) return;             /* 根页跳过 */
    /* 首页：toctree 用 <self> 自引用 → 仅 1 个 current 且 href 为 "#"
       面包屑和"最后更新"对首页是冗余信息，直接跳过 */
    if (currentLis.length === 1) {
      var firstLink = currentLis[0].querySelector(':scope > a');
      if (firstLink && firstLink.getAttribute('href') === '#') return;
    }

    var prefix = langPrefix();

    /* —— 面包屑 —— */
    var nav = document.createElement('nav');
    nav.className = 'mo-breadcrumb';
    nav.setAttribute('aria-label', 'breadcrumb');

    var html = '<a class="mo-breadcrumb__link mo-breadcrumb__home" href="' + prefix +
               '" aria-label="' + T.home + '">' + HOME_SVG + '</a>';

    currentLis.forEach(function (li, idx) {
      var a = li.querySelector(':scope > a');
      if (!a) return;
      var label = (a.textContent || '').trim();
      if (!label) return;
      var isLast = idx === currentLis.length - 1;
      html += '<span class="mo-breadcrumb__sep">' + CHEVRON_SVG + '</span>';
      html += isLast
        ? '<span class="mo-breadcrumb__current">' + escapeHtml(label) + '</span>'
        : '<a class="mo-breadcrumb__link" href="' + a.getAttribute('href') + '">' + escapeHtml(label) + '</a>';
    });

    nav.innerHTML = html;
    article.insertBefore(nav, article.firstChild);

    /* —— 更新时间 —— */
    var meta = document.createElement('div');
    meta.className = 'mo-lastupdated';
    meta.innerHTML = T.updatedPrefix + '<strong>' + formatDate(fakeDate(location.pathname)) + '</strong>';
    article.insertBefore(meta, nav.nextSibling);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
