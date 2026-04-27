"""MatrixOne Intelligence English docs (demo, partial — only 4 core docs translated).

继承 matrixone 中文站（matrixone/conf.py）的全部 Sphinx / MyST / Furo 配置，
不通过 intelligence/conf.py 中转（避免 conf.py 同名循环），重复一行 icons.js
追加是可以接受的代价。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "matrixone"))

from conf import *  # noqa: F401, F403, E402

project = "MatrixOne Intelligence Docs"
html_title = "MatrixOne Intelligence Docs"
copyright = "2026, MatrixOne"
language = "en"

# 同 intelligence/conf.py：首页 4 张卡片用 lucide 线性 SVG 图标
html_js_files = list(html_js_files) + ["js/icons.js"]  # noqa: F405
