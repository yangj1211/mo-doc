/* 多列功能页脚 —— append 到 body 末尾，全宽显示在页面最底部
   - 上方：4 列功能导航（产品 / 资源 / 社区 / 公司）
   - 下方：logo + 版权 + ICP 备案 + 法律链接
   - 取代 Furo 默认那行 "Made with Sphinx and Furo"（已经在 CSS 里隐藏了 .bottom-of-page）
   - 维护：i18n 字典在文件顶部，链接列表也都在那里 */
(function () {
  'use strict';
  if (document.querySelector('.mo-footer')) return;

  var LANG = (document.documentElement.lang || '').toLowerCase().indexOf('en') === 0 ? 'en' : 'zh';

  function langPrefix() {
    /* URL 形如 /<product>/<lang>/...；返回 "/<product>/<lang>/" */
    var m = location.pathname.match(/^(\/[a-z][a-z0-9-]+\/(?:zh|en))(?:\/|$)/);
    return m ? m[1] + '/' : '/' + LANG + '/';
  }

  var T = LANG === 'en' ? {
    cols: [
      { title: 'Product', items: [
        { label: 'Overview',     href: 'https://www.matrixorigin.cn/product' },
        { label: 'Solutions',    href: 'https://www.matrixorigin.cn/solutions' },
        { label: 'Customers',    href: 'https://www.matrixorigin.cn/customers' },
        { label: 'Pricing',      href: 'https://www.matrixorigin.cn/pricing' }
      ]},
      { title: 'Resources', items: [
        { label: 'Docs',         href: '/' },
        { label: 'Blog',         href: 'https://www.matrixorigin.cn/blog' },
        { label: 'Whitepapers',  href: '#' },
        { label: 'Status',       href: '#' }
      ]},
      { title: 'Community', items: [
        { label: 'GitHub',       href: 'https://github.com/matrixorigin/matrixone' },
        { label: 'Zhihu',        href: '#' },
        { label: 'WeChat group', href: '#' },
        { label: 'Forum',        href: '#' }
      ]},
      { title: 'Company', items: [
        { label: 'About',        href: 'https://www.matrixorigin.cn/about' },
        { label: 'Careers',      href: 'https://www.matrixorigin.cn/careers' },
        { label: 'Contact',      href: 'https://www.matrixorigin.cn/contact' },
        { label: 'Partners',     href: '#' }
      ]}
    ],
    copyright: '© 2026 MatrixOrigin. All rights reserved.',
    icp: [
      { label: '沪ICP备XXXXXXXX号', href: 'https://beian.miit.gov.cn' },
      { label: '沪公网安备 XXXXXXXXXXXXXX 号', href: '#' }
    ],
    legal: [
      { label: 'Privacy',  href: '#' },
      { label: 'Terms',    href: '#' },
      { label: 'Cookies',  href: '#' }
    ]
  } : {
    cols: [
      { title: '产品', items: [
        { label: '产品概述',     href: 'https://www.matrixorigin.cn/product' },
        { label: '解决方案',     href: 'https://www.matrixorigin.cn/solutions' },
        { label: '客户案例',     href: 'https://www.matrixorigin.cn/customers' },
        { label: '定价',         href: 'https://www.matrixorigin.cn/pricing' }
      ]},
      { title: '资源', items: [
        { label: '文档中心',     href: '/' },
        { label: '技术博客',     href: 'https://www.matrixorigin.cn/blog' },
        { label: '白皮书下载',   href: '#' },
        { label: '系统状态',     href: '#' }
      ]},
      { title: '社区', items: [
        { label: 'GitHub',       href: 'https://github.com/matrixorigin/matrixone' },
        { label: '知乎专栏',     href: '#' },
        { label: '微信群',       href: '#' },
        { label: '技术论坛',     href: '#' }
      ]},
      { title: '公司', items: [
        { label: '关于我们',     href: 'https://www.matrixorigin.cn/about' },
        { label: '加入我们',     href: 'https://www.matrixorigin.cn/careers' },
        { label: '联系我们',     href: 'https://www.matrixorigin.cn/contact' },
        { label: '合作伙伴',     href: '#' }
      ]}
    ],
    copyright: '© 2026 MatrixOrigin. 保留所有权利。',
    icp: [
      { label: '沪ICP备XXXXXXXX号', href: 'https://beian.miit.gov.cn' },
      { label: '沪公网安备 XXXXXXXXXXXXXX 号', href: '#' }
    ],
    legal: [
      { label: '隐私政策',     href: '#' },
      { label: '服务条款',     href: '#' },
      { label: 'Cookie 设置',  href: '#' }
    ]
  };

  function escapeHtml(s) {
    return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function build() {
    var prefix = langPrefix();

    var gridHtml = T.cols.map(function (col) {
      var lis = col.items.map(function (it) {
        var ext = /^https?:/.test(it.href) ? ' target="_blank" rel="noopener"' : '';
        return '<li><a href="' + it.href + '"' + ext + '>' + escapeHtml(it.label) + '</a></li>';
      }).join('');
      return '<div class="mo-footer-col">' +
               '<h4 class="mo-footer-title">' + escapeHtml(col.title) + '</h4>' +
               '<ul>' + lis + '</ul>' +
             '</div>';
    }).join('');

    var icpHtml = T.icp.map(function (it, i) {
      var ext = /^https?:/.test(it.href) ? ' target="_blank" rel="noopener"' : '';
      return (i > 0 ? '<span class="mo-footer-sep">·</span>' : '') +
             '<a href="' + it.href + '"' + ext + '>' + escapeHtml(it.label) + '</a>';
    }).join('');

    var legalHtml = T.legal.map(function (it, i) {
      return (i > 0 ? '<span class="mo-footer-sep">·</span>' : '') +
             '<a href="' + it.href + '">' + escapeHtml(it.label) + '</a>';
    }).join('');

    var footer = document.createElement('footer');
    footer.className = 'mo-footer';
    footer.innerHTML =
      '<div class="mo-footer-inner">' +
        '<div class="mo-footer-grid">' + gridHtml + '</div>' +
        '<div class="mo-footer-divider"></div>' +
        '<div class="mo-footer-bottom">' +
          '<div class="mo-footer-bottom-left">' +
            '<img src="' + prefix + '_static/images/matrixone-logo-light.svg" ' +
                 'class="mo-footer-logo mo-footer-logo--light" alt="MatrixOrigin" />' +
            '<img src="' + prefix + '_static/images/matrixone-logo-dark.svg" ' +
                 'class="mo-footer-logo mo-footer-logo--dark" alt="MatrixOrigin" />' +
            '<span class="mo-footer-copyright">' + escapeHtml(T.copyright) + '</span>' +
          '</div>' +
          '<div class="mo-footer-bottom-center">' + icpHtml + '</div>' +
          '<div class="mo-footer-bottom-right">' + legalHtml + '</div>' +
        '</div>' +
      '</div>';

    document.body.appendChild(footer);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
