"""English Sphinx build.

Inherits everything from the Chinese conf.py (``source/conf.py``) and only
overrides the language and site title. Keeping both confs in lockstep this
way means any new extension or option added in Chinese is picked up
automatically by the English build.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "source"))

from conf import *  # noqa: F401, F403, E402

language = "en"
html_title = "MatrixOne Docs"
