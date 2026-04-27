"""MatrixOne 文档(中英共用 conf.py)

源内容分别在 source/zh 与 source/en;sphinx-build 的位置参数指定走哪一套。
通过 SPHINX_LANG 环境变量(zh_CN | en)切换 language 与品牌标题,
Makefile 会在调用前 export SPHINX_LANG。
"""
import os

_lang = os.environ.get("SPHINX_LANG", "zh_CN")

project = "MatrixOne Docs" if _lang == "en" else "MatrixOne 文档"
html_title = project
author = "MatrixOne"
copyright = "2026, MatrixOne"
language = _lang

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
html_static_path = ["source/_static"]
templates_path = ["source/_templates"]
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
]

html_show_sourcelink = False
html_copy_source = False

html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#004af0",
        "color-brand-content": "#004af0",
    },
    "dark_css_variables": {
        "color-brand-primary": "#6b8cff",
        "color-brand-content": "#6b8cff",
    },
    "sidebar_hide_name": False,
}
