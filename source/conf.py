project = "MatrixOne 文档"
author = "MatrixOne"
copyright = "2026, MatrixOne"
language = "zh_CN"

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
    # demo 只迁移了 Release-Notes / Overview / FAQs 三个目录，
    # 这些目录内会有指向未迁移章节（Deploy / Reference / Maintain / Develop 等）的链接。
    # 不作为 build 噪音处理；研发做全量迁移时取消这两行即可逐个审。
    "myst.xref_missing",
    "myst.header",
]

html_theme = "furo"
html_title = "MatrixOne 文档"
html_static_path = ["_static"]
html_css_files = ["css/custom.css"]
html_js_files = ["js/topbar.js", "js/breadcrumb.js", "js/feedback.js", "js/footer.js", "js/mo-highlight.js", "js/assistant.js", "js/lang-switcher.js"]

# demo 不需要暴露 Markdown 源文件入口（也避免 python http.server 的 .txt charset 坑）
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
