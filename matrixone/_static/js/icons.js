/* 入口卡片图标注入（intelligence 子站首页用）
   - 找到所有 .mo-entry-card，按 DOM 顺序在前 4 张前面注入 SVG 图标块
   - 图标取自 lucide.dev（线性、stroke="currentColor"），已内联无外部依赖
   - 配色由 CSS 控制（.mo-card-icon），在浅色/暗色 / hover 三个态都自适应
   - 当页面里没有 .mo-entry-card（任何非首页文档），脚本是 no-op */
(function () {
  'use strict';

  var SVG_HEAD =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor"' +
    ' stroke-width="2" stroke-linecap="round" stroke-linejoin="round"' +
    ' aria-hidden="true">';
  var SVG_TAIL = '</svg>';

  /* lucide icons：rocket / lightbulb / code / help-circle */
  var ICONS = {
    rocket:
      '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91' +
      'a2.18 2.18 0 0 0-2.91-.09z"/>' +
      '<path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2' +
      'c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/>' +
      '<path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/>' +
      '<path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>',
    lightbulb:
      '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8' +
      'c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/>' +
      '<path d="M9 18h6"/>' +
      '<path d="M10 22h4"/>',
    code:
      '<polyline points="16 18 22 12 16 6"/>' +
      '<polyline points="8 6 2 12 8 18"/>',
    help:
      '<circle cx="12" cy="12" r="10"/>' +
      '<path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/>' +
      '<path d="M12 17h.01"/>'
  };

  /* 顺序对应主页 4 张卡片：5 分钟上手 / 核心概念 / API 参考 / 常见问题 */
  var ORDER = ['rocket', 'lightbulb', 'code', 'help'];

  function build() {
    var cards = document.querySelectorAll('.mo-entry-card');
    if (!cards.length) return;
    cards.forEach(function (card, i) {
      if (i >= ORDER.length) return;
      if (card.querySelector('.mo-card-icon')) return;
      var body = card.querySelector('.sd-card-body') || card;
      var iconEl = document.createElement('div');
      iconEl.className = 'mo-card-icon';
      iconEl.innerHTML = SVG_HEAD + ICONS[ORDER[i]] + SVG_TAIL;
      body.insertBefore(iconEl, body.firstChild);
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
