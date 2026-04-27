/* 版本切换 pill —— 当前只是占位,下拉里只有 latest。
   多版本归档功能上线后,在 VERSIONS 数组里追加版本即可。
   - 注入到 .theme-toggle-container,排在语言 pill 左侧
   - 下拉用 click 切换 .is-open 类,纯 CSS 控制可见
   - 点击外部自动收起 */
(function () {
  'use strict';

  var LANG = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0 ? 'en' : 'zh';
  var T = LANG === 'en' ? {
    heading: 'Documentation version',
    hint: 'Archived versions coming soon'
  } : {
    heading: '文档版本',
    hint: '历史版本归档功能开发中,敬请期待'
  };

  var VERSIONS = [{ label: 'latest', active: true }];

  var CHEVRON =
    '<svg class="mo-version-pill__chevron" viewBox="0 0 12 12" aria-hidden="true">' +
      '<path d="M3 4.5l3 3 3-3" fill="none" stroke="currentColor" ' +
      'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>' +
    '</svg>';

  var CHECK =
    '<svg viewBox="0 0 12 12" aria-hidden="true">' +
      '<path d="M2.5 6l2.5 2.5 4.5-5" fill="none" stroke="currentColor" ' +
      'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>' +
    '</svg>';

  function renderItems() {
    return VERSIONS.map(function (v) {
      return '<div class="mo-version-menu__item' + (v.active ? ' is-active' : '') +
             '" role="option" aria-selected="' + !!v.active + '">' +
               '<span>' + v.label + '</span>' +
               (v.active ? CHECK : '') +
             '</div>';
    }).join('');
  }

  function buildOne(container) {
    if (container.querySelector('.mo-version-switcher')) return;

    var wrap = document.createElement('div');
    wrap.className = 'mo-version-switcher';
    wrap.innerHTML =
      '<button type="button" class="mo-version-pill" aria-haspopup="listbox" aria-expanded="false">' +
        '<span class="mo-version-pill__label">latest</span>' +
        CHEVRON +
      '</button>' +
      '<div class="mo-version-menu" role="listbox">' +
        '<div class="mo-version-menu__heading">' + T.heading + '</div>' +
        renderItems() +
        '<div class="mo-version-menu__hint">' + T.hint + '</div>' +
      '</div>';

    var anchor = container.querySelector('.mo-lang-pill') || container.querySelector('.theme-toggle');
    if (anchor) container.insertBefore(wrap, anchor);
    else container.appendChild(wrap);

    var btn = wrap.querySelector('.mo-version-pill');
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var open = wrap.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      /* 关掉其它已展开的实例(桌面/移动各一个) */
      document.querySelectorAll('.mo-version-switcher.is-open').forEach(function (w) {
        if (w !== wrap) {
          w.classList.remove('is-open');
          w.querySelector('.mo-version-pill').setAttribute('aria-expanded', 'false');
        }
      });
    });
  }

  function build() {
    var containers = document.querySelectorAll('.theme-toggle-container');
    if (!containers.length) return;
    containers.forEach(buildOne);
  }

  document.addEventListener('click', function () {
    document.querySelectorAll('.mo-version-switcher.is-open').forEach(function (w) {
      w.classList.remove('is-open');
      w.querySelector('.mo-version-pill').setAttribute('aria-expanded', 'false');
    });
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
