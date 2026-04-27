"""MatrixOne Intelligence 文档（demo 子站）

继承 matrixone 中文站（matrixone/conf.py）的全部 Sphinx / MyST / Furo 配置，
只覆盖品牌字段（产品名 / 标题 / copyright）。

主题色、扩展、JS/CSS 列表、suppress_warnings 全部沿用 matrixone，
任何主题层升级在 matrixone 改一处，intelligence 自动跟随。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "matrixone"))

from conf import *  # noqa: F401, F403, E402

project = "MatrixOne Intelligence 文档"
html_title = "MatrixOne Intelligence 文档"
copyright = "2026, MatrixOne"

# intelligence 子站独有：首页 4 张入口卡片用 lucide 线性 SVG 图标（紫色调）。
# icons.js 由 JS 注入 SVG，仅在含 .mo-entry-card 的页面生效（即 intelligence 首页）。
html_js_files = list(html_js_files) + ["js/icons.js"]  # noqa: F405
