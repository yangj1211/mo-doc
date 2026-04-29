"""MatrixOne 文档(中英共用 conf.py)。

主题/扩展/MyST 配置全部继承自 _shared_theme/conf_base.py。
本文件只声明产品维度:
- 项目名/标题(随 SPHINX_LANG 切语种)
- 内容 language
- 主题资源路径(指回 ../_shared_theme/)
- html_context.product = 'matrixone' → CSS 用 [data-product="matrixone"] 选品牌色
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "_shared_theme"))

from conf_base import *  # noqa: F401, F403, E402

_lang = os.environ.get("SPHINX_LANG", "zh_CN")

project = "MatrixOne Docs" if _lang == "en" else "MatrixOne 文档"
html_title = project
author = "MatrixOne"
copyright = "2026, MatrixOne"
language = _lang

html_static_path = ["../_shared_theme/_static"]
templates_path = ["../_shared_theme/_templates"]

html_context = {"product": "matrixone"}
