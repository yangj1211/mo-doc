/* MatrixOne 方言关键字二次高亮
   Pygments 的 SQL / bash lexer 不识别 MatrixOne 专有关键字（SNAPSHOT / CLONE / DATA BRANCH 等）。
   本脚本在页面加载后扫描代码块的 innerHTML，把方言关键字包成 <span class="mo-keyword">，
   CSS 再把它染成品牌紫 + 加粗，和普通 SQL 关键字（GitHub 蓝）区分开。

   ★ 维护：新增方言词只改下面 DIALECT_PHRASES / DIALECT_WORDS 即可。 */
(function () {
  'use strict';

  /* 多词短语（按长度降序，先匹配长的避免被单词截断吃掉） */
  var DIALECT_PHRASES = [
    'FOR SYSTEM_TIME',
    'RESTORE FROM SNAPSHOT',
    'RESTORE FROM PITR',
    'CREATE SNAPSHOT',
    'DROP SNAPSHOT',
    'SHOW SNAPSHOTS',
    'CREATE PITR',
    'DROP PITR',
    'ALTER PITR',
    'SHOW PITRS',
    'WHEN CONFLICT',
    'MERGE INTO',
    'DATA BRANCH',
    'CREATE BRANCH',
    'DROP BRANCH'
  ];

  /* 单词级方言词 */
  var DIALECT_WORDS = [
    'SNAPSHOT', 'SNAPSHOTS',
    'CLONE', 'CLONES',
    'BRANCH', 'BRANCHES',
    'DATABRANCH',
    'PITR', 'PITRS',
    'RESTORE',
    'VECF32', 'VECF64',
    'CDC',
    'HTAP', 'HSTAP'
  ];

  /* 需要处理的代码块语言 */
  var TARGET_SELECTORS = [
    '.highlight-sql pre',
    '.highlight-mysql pre',
    '.highlight-bash pre',
    '.highlight-zsh pre',
    '.highlight-sh pre',
    '.highlight-shell pre',
    '.highlight-text pre',
    '.highlight-default pre'
  ];

  function escapeRegex(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }

  /* 短语正则：允许 word 之间有空白 + 可选 HTML 标签（Pygments 可能把相邻 token 分成多个 span） */
  function phraseRegex(phrase) {
    var tokens = phrase.split(/\s+/).map(escapeRegex);
    var sep = '(?:\\s|<[^<>]*>)+';
    return new RegExp('\\b' + tokens.join(')' + sep + '(') + '\\b', 'gi').source
           .replace(/^\\b\(/, '\\b')
           .replace(/\)\\b$/, '\\b');
  }

  /* 构建一次所有短语的 RegExp */
  function buildPhraseRes() {
    return DIALECT_PHRASES.map(function (p) {
      var tokens = p.split(/\s+/).map(escapeRegex);
      var sep = '(?:\\s|<[^<>]*>)+';
      return new RegExp('\\b' + tokens.join(sep) + '\\b', 'gi');
    });
  }
  var PHRASE_RES = buildPhraseRes();

  /* 用 split 排除已被 .mo-keyword 包裹的片段后，再做单词级替换 */
  function wrapWords(html) {
    var parts = html.split(/(<span class="mo-keyword">[\s\S]*?<\/span>)/g);
    for (var i = 0; i < parts.length; i++) {
      if (parts[i].indexOf('class="mo-keyword"') !== -1) continue;
      DIALECT_WORDS.forEach(function (w) {
        var re = new RegExp('\\b' + escapeRegex(w) + '\\b', 'g');
        parts[i] = parts[i].replace(re, function (m) {
          return '<span class="mo-keyword">' + m + '</span>';
        });
      });
    }
    return parts.join('');
  }

  function process(pre) {
    var html = pre.innerHTML;
    var original = html;

    /* 短语先行，整段包成 mo-keyword（包括中间可能夹着的现有 span） */
    PHRASE_RES.forEach(function (re) {
      html = html.replace(re, function (m) {
        return '<span class="mo-keyword">' + m + '</span>';
      });
    });

    /* 单词级，仅处理未被包裹的部分 */
    html = wrapWords(html);

    if (html !== original) pre.innerHTML = html;
  }

  function run() {
    var blocks = document.querySelectorAll(TARGET_SELECTORS.join(','));
    blocks.forEach(process);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', run);
  } else {
    run();
  }
})();
