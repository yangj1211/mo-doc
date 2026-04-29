/* 代码块折叠 + 全屏 —— Snowflake 风
   - 超过 12 行的代码块默认收到 320px 高度,底部渐变蒙版,正中浮"展开"按钮
   - 右上角加一个全屏按钮(在复制按钮左侧 32px 处),弹出模态框看完整代码
   - 短代码块不加任何按钮,保持原貌

   加载在 sphinx-copybutton.js 之后,所以执行时复制按钮已经注入,
   两个按钮相邻不冲突(copybtn @ right:12, fullscreen @ right:44)。 */
(function () {
  'use strict';

  var COLLAPSE_LINE_THRESHOLD = 12;
  var COLLAPSED_HEIGHT_PX = 320;

  var ICON_DOWN =
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<polyline points="7 13 12 18 17 13"/><polyline points="7 6 12 11 17 6"/></svg>';
  var ICON_UP =
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<polyline points="17 11 12 6 7 11"/><polyline points="17 18 12 13 7 18"/></svg>';
  var ICON_EXPAND_FS =
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/>' +
    '<line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></svg>';
  var ICON_CLOSE =
    '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>';

  var EXPAND_LABEL_ZH = '展开';
  var COLLAPSE_LABEL_ZH = '收起';
  var EXPAND_LABEL_EN = 'Expand';
  var COLLAPSE_LABEL_EN = 'Collapse';
  var LANG = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0 ? 'en' : 'zh';
  var EXPAND_LABEL = LANG === 'en' ? EXPAND_LABEL_EN : EXPAND_LABEL_ZH;
  var COLLAPSE_LABEL = LANG === 'en' ? COLLAPSE_LABEL_EN : COLLAPSE_LABEL_ZH;

  function makeExpandBtn(block) {
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'mo-code-expand-btn';
    btn.setAttribute('aria-expanded', 'false');
    btn.innerHTML = '<span class="mo-code-expand-btn__icon">' + ICON_DOWN + '</span>' +
                    '<span class="mo-code-expand-btn__label">' + EXPAND_LABEL + '</span>';

    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var collapsed = block.classList.contains('mo-code-collapsed');
      if (collapsed) {
        block.classList.remove('mo-code-collapsed');
        block.style.maxHeight = 'none';
        btn.setAttribute('aria-expanded', 'true');
        btn.querySelector('.mo-code-expand-btn__icon').innerHTML = ICON_UP;
        btn.querySelector('.mo-code-expand-btn__label').textContent = COLLAPSE_LABEL;
      } else {
        block.classList.add('mo-code-collapsed');
        block.style.maxHeight = COLLAPSED_HEIGHT_PX + 'px';
        btn.setAttribute('aria-expanded', 'false');
        btn.querySelector('.mo-code-expand-btn__icon').innerHTML = ICON_DOWN;
        btn.querySelector('.mo-code-expand-btn__label').textContent = EXPAND_LABEL;
        // 折叠后让用户视线回到代码块顶部,不然停在中间页面体验差
        block.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
    return btn;
  }

  function makeFullscreenBtn(block) {
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'mo-code-fullscreen-btn';
    btn.title = LANG === 'en' ? 'View fullscreen' : '全屏查看';
    btn.setAttribute('aria-label', btn.title);
    btn.innerHTML = ICON_EXPAND_FS;
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      openFullscreen(block);
    });
    return btn;
  }

  function openFullscreen(block) {
    var overlay = document.createElement('div');
    overlay.className = 'mo-code-overlay';
    overlay.setAttribute('role', 'dialog');
    overlay.setAttribute('aria-modal', 'true');

    var modal = document.createElement('div');
    modal.className = 'mo-code-modal';

    var closeBtn = document.createElement('button');
    closeBtn.type = 'button';
    closeBtn.className = 'mo-code-close-btn';
    closeBtn.title = LANG === 'en' ? 'Close (Esc)' : '关闭 (Esc)';
    closeBtn.setAttribute('aria-label', closeBtn.title);
    closeBtn.innerHTML = ICON_CLOSE;

    var clone = block.cloneNode(true);
    /* 模态里不要再有折叠/全屏控件,也不要 max-height 限制 */
    clone.classList.remove('mo-code-collapsed', 'mo-code-collapsible');
    clone.style.maxHeight = 'none';
    clone.style.overflow = 'visible';
    var btns = clone.querySelectorAll('.mo-code-expand-btn, .mo-code-fullscreen-btn');
    for (var i = 0; i < btns.length; i++) btns[i].parentNode.removeChild(btns[i]);

    modal.appendChild(closeBtn);
    modal.appendChild(clone);
    overlay.appendChild(modal);
    document.body.appendChild(overlay);
    document.body.classList.add('mo-code-modal-open');

    function close() {
      overlay.parentNode && overlay.parentNode.removeChild(overlay);
      document.body.classList.remove('mo-code-modal-open');
      document.removeEventListener('keydown', onKey);
    }
    function onKey(e) {
      if (e.key === 'Escape') close();
    }

    closeBtn.addEventListener('click', close);
    overlay.addEventListener('click', function (e) {
      if (e.target === overlay) close();
    });
    document.addEventListener('keydown', onKey);
  }

  function init() {
    /* sphinx-design tab-set 内的代码块也要支持(用 div.highlight 通用选择)。
       但要避开模态框里的 clone(后挂到 body,init 已经跑完,不会重入)。 */
    var blocks = document.querySelectorAll('div.highlight');
    blocks.forEach(function (block) {
      if (block.classList.contains('mo-code-collapsible')) return; // 已处理过
      var pre = block.querySelector('pre');
      if (!pre) return;

      var lines = pre.textContent.replace(/\n+$/, '').split('\n').length;
      if (lines <= COLLAPSE_LINE_THRESHOLD) return;

      block.classList.add('mo-code-collapsible', 'mo-code-collapsed');
      block.style.maxHeight = COLLAPSED_HEIGHT_PX + 'px';

      block.appendChild(makeExpandBtn(block));
      block.appendChild(makeFullscreenBtn(block));
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
