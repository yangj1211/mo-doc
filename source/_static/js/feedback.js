/* 右侧 TOC 下方的反馈区 + GitHub 编辑链接（Databricks 风格紧凑版）
   - 注入到 .toc-sticky 末尾，按 [TOC] [反馈] [编辑此页] 顺序排列
   - 标题 + Yes/No（横向并排）+ 发送反馈（独立一行）
   - 点 Yes → 直接感谢；点 No 或"发送反馈" → 高亮 + 展开 textarea + 提交
   - 后端预留：window.MODocsFeedback.submit(pageUrl, type, comment) */
(function () {
  'use strict';
  if (document.querySelector('.mo-sidebar-feedback')) return;

  var LANG = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0 ? 'en' : 'zh';
  var T = LANG === 'en' ? {
    question: 'Was this page helpful?',
    yes: 'Helpful',
    no: 'Not helpful',
    sendFeedback: 'Send feedback',
    detailPlaceholder: 'Tell us...',
    submit: 'Submit',
    thanks: '✓ Thanks!',
    editOnGithub: 'Edit this page on GitHub'
  } : {
    question: '这页文档对你有帮助吗？',
    yes: '有帮助',
    no: '没帮助',
    sendFeedback: '发送反馈',
    detailPlaceholder: '告诉我们...',
    submit: '提交',
    thanks: '✓ 感谢反馈',
    editOnGithub: '在 GitHub 上编辑此页'
  };

  /* 后端 hook：默认 noop */
  if (!window.MODocsFeedback) {
    window.MODocsFeedback = {
      submit: function (pageUrl, type, comment) {
        if (window.console && console.log) {
          console.log('[demo] feedback', { pageUrl: pageUrl, type: type, comment: comment });
        }
      }
    };
  }

  /* —— inline SVG（Lucide 风格，14px，跟随 currentColor） —— */
  var THUMB_UP =
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<path d="M7 10v12"/>' +
      '<path d="M15 5.88L14 10h5.83a2 2 0 0 1 1.92 2.56l-2.33 8A2 2 0 0 1 17.5 22H4a2 2 0 0 1-2-2v-8a2 2 0 0 1 2-2h2.76a2 2 0 0 0 1.79-1.11L12 2a3.13 3.13 0 0 1 3 3.88z"/>' +
    '</svg>';
  var THUMB_DOWN =
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<path d="M17 14V2"/>' +
      '<path d="M9 18.12L10 14H4.17a2 2 0 0 1-1.92-2.56l2.33-8A2 2 0 0 1 6.5 2H20a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2h-2.76a2 2 0 0 0-1.79 1.11L12 22a3.13 3.13 0 0 1-3-3.88z"/>' +
    '</svg>';
  var MESSAGE_ICON =
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>' +
    '</svg>';
  var EDIT_ICON =
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" ' +
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
      '<path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>' +
      '<path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>' +
    '</svg>';

  function buildEditUrl() {
    var path = location.pathname
      .replace(/^\/(zh|en)\//, '')
      .replace(/\.html$/, '.md')
      .replace(/(^|\/)$/, '$1index.md');
    return 'https://github.com/matrixorigin/matrixorigin.io.cn/edit/main/docs/MatrixOne/' + path;
  }

  function build() {
    /* 找右侧 TOC 容器；如果没有 TOC（比如 index 页），就放到侧边栏 drawer 里 */
    var sticky = document.querySelector('.toc-sticky');
    if (!sticky) return;

    /* —— 反馈区 —— */
    var fb = document.createElement('div');
    fb.className = 'mo-sidebar-feedback';
    fb.innerHTML =
      '<h4 class="mo-sidebar-feedback-title">' + T.question + '</h4>' +
      '<div class="mo-sidebar-feedback-buttons">' +
        '<button type="button" class="mo-sidebar-feedback-btn" data-feedback="yes">' +
          THUMB_UP + '<span>' + T.yes + '</span>' +
        '</button>' +
        '<button type="button" class="mo-sidebar-feedback-btn" data-feedback="no">' +
          THUMB_DOWN + '<span>' + T.no + '</span>' +
        '</button>' +
      '</div>' +
      '<button type="button" class="mo-sidebar-feedback-btn mo-sidebar-feedback-btn-full" data-feedback="detail">' +
        MESSAGE_ICON + '<span>' + T.sendFeedback + '</span>' +
      '</button>' +
      '<div class="mo-sidebar-feedback-detail" hidden>' +
        '<textarea placeholder="' + T.detailPlaceholder + '" maxlength="500"></textarea>' +
        '<button type="button" class="mo-sidebar-feedback-submit">' + T.submit + '</button>' +
      '</div>' +
      '<div class="mo-sidebar-feedback-thanks" hidden>' + T.thanks + '</div>';
    sticky.appendChild(fb);

    /* —— GitHub 编辑链接 —— */
    var edit = document.createElement('div');
    edit.className = 'mo-sidebar-edit';
    edit.innerHTML =
      '<a href="' + buildEditUrl() + '" target="_blank" rel="noopener">' +
        EDIT_ICON + '<span>' + T.editOnGithub + '</span>' +
      '</a>';
    sticky.appendChild(edit);

    /* —— 交互 —— */
    var title = fb.querySelector('.mo-sidebar-feedback-title');
    var btnRow = fb.querySelector('.mo-sidebar-feedback-buttons');
    var btnFull = fb.querySelector('.mo-sidebar-feedback-btn-full');
    var detail = fb.querySelector('.mo-sidebar-feedback-detail');
    var thanks = fb.querySelector('.mo-sidebar-feedback-thanks');
    var textarea = fb.querySelector('textarea');
    var submitBtn = fb.querySelector('.mo-sidebar-feedback-submit');
    var allBtns = fb.querySelectorAll('.mo-sidebar-feedback-btn');
    var lastType = 'no';

    function clearActive() {
      allBtns.forEach(function (b) { b.classList.remove('active'); });
    }
    function showThanks() {
      title.hidden = true;
      btnRow.hidden = true;
      btnFull.hidden = true;
      detail.hidden = true;
      thanks.hidden = false;
    }

    allBtns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var type = btn.getAttribute('data-feedback');
        if (type === 'yes') {
          window.MODocsFeedback.submit(location.pathname, 'yes', '');
          showThanks();
        } else {
          clearActive();
          btn.classList.add('active');
          lastType = type;
          detail.hidden = false;
          setTimeout(function () { textarea.focus(); }, 50);
        }
      });
    });

    submitBtn.addEventListener('click', function () {
      window.MODocsFeedback.submit(location.pathname, lastType, textarea.value);
      showThanks();
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
