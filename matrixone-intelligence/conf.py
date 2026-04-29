"""MatrixOne Intelligence 文档(中英共用 conf.py)。

跟 matrixone/conf.py 一样从 _shared_theme/conf_base.py 继承,
只是产品名/品牌槽不同,并追加首页 4 张入口卡片用的 lucide SVG 图标 JS。
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "_shared_theme"))

from conf_base import *  # noqa: F401, F403, E402

_lang = os.environ.get("SPHINX_LANG", "zh_CN")

project = "MatrixOne Intelligence Docs" if _lang == "en" else "MatrixOne Intelligence 文档"
html_title = project
author = "MatrixOne"
copyright = "2026, MatrixOne"
language = _lang

html_static_path = ["../_shared_theme/_static"]
templates_path = ["../_shared_theme/_templates"]

# CSS 用 [data-product="intelligence"] 选择紫色调品牌槽
html_context = {"product": "intelligence"}

# intelligence 子站独有:首页 4 张入口卡片用 lucide 线性 SVG 图标(紫色调)
# icons.js 由 JS 注入 SVG,仅在含 .mo-entry-card 的页面生效(即 intelligence 首页)
html_js_files = list(html_js_files) + ["js/icons.js"]  # noqa: F405
