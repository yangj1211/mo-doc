"""共享 Sphinx / MyST / Furo 配置 —— 所有产品继承,不要在这里写产品特定的字段。

每个产品的 conf.py 只需要:
    import sys, os
    sys.path.insert(0, os.path.abspath('../_shared_theme'))
    from conf_base import *

    project = "..."
    html_title = project
    html_context = {"product": "<slug>"}    # 决定 CSS 走哪一套品牌色

不要在这里设 project / html_title / language / html_context —— 这些是产品维度。
不要在这里写 html_static_path / templates_path —— 路径相对各产品的 confdir 不同,
由产品 conf.py 写 ['../_shared_theme/_static'] / ['../_shared_theme/_templates']。
"""

extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "attrs_block",
    "tasklist",
]

source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

suppress_warnings = [
    "misc.highlighting_failure",
    "myst.xref_missing",
    "myst.header",
]

html_theme = "furo"

# 路径相对 confdir(= 各产品目录)。两个产品的 conf.py 都会显式重新声明这两项,
# 这里给一个默认值,防止从某个未声明的 conf.py 直接 sphinx-build 时报错。
html_static_path = ["../_shared_theme/_static"]
templates_path = ["../_shared_theme/_templates"]

html_css_files = ["css/custom.css"]
html_js_files = [
    "js/topbar.js",
    "js/breadcrumb.js",
    "js/feedback.js",
    "js/footer.js",
    "js/mo-highlight.js",
    "js/assistant.js",
    "js/lang-switcher.js",
    "js/version-switcher.js",
    # 必须在 sphinx-copybutton 之后,扫描代码块时复制按钮已就位 → 全屏按钮位置
    # 不冲突。html_js_files 在 sphinx 内置 + 扩展资源(含 copybutton.js)之后渲染,
    # 所以列表末尾就是最后执行,顺序天然正确。
    "js/code-collapse.js",
]

html_show_sourcelink = False
html_copy_source = False

html_theme_options = {
    "light_css_variables": {
        # color-brand-primary / color-brand-content 由 custom.css 的 :root 覆盖,
        # 这里只是给一个 furo 默认 fallback。
        "color-brand-primary": "#004af0",
        "color-brand-content": "#004af0",
    },
    "dark_css_variables": {
        "color-brand-primary": "#6b8cff",
        "color-brand-content": "#6b8cff",
    },
    "sidebar_hide_name": False,
}
