#!/usr/bin/env python3
"""IA 迁移补丁:第一次跑 migrate_ia.py 时 write-back 比较错了 buffer,
导致只有同时改了 toctree 的文件被写回;只改了 markdown link 的文件没写。

这一遍走每个 .md 在 NEW 位置上的链接,逐个判断:
  - 如果 link 在 NEW 形式下能 resolve 到现存文件 → skip
  - 否则按"link 是 OLD 形式,文件位于 OLD 位置"重新解释,recompute
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "matrixone" / "source"
LANGS = ["zh", "en"]

# (new_prefix, old_prefix) —— 反向 remap;顺序:更长 prefix 先
REVERSE = [
    ("operate/performance", "performance-tuning"),
    ("operate/deploy", "deploy"),
    ("operate/maintain", "maintain"),
    ("operate/migrate", "migrate"),
    ("operate/security", "security"),
    ("operate/test", "test"),
    ("help/troubleshooting", "troubleshooting"),
    ("help/faqs", "faqs"),
    ("develop/tutorials", "tutorial"),
    ("get-started", "getting-started"),
    ("reference", "sql-reference"),
    ("concepts/glossary.md", "glossary.md"),
    ("concepts", "overview"),
]
# remap (old → new) 同 migrate_ia.py
FORWARD = [
    ("performance-tuning", "operate/performance"),
    ("getting-started", "get-started"),
    ("sql-reference", "reference"),
    ("troubleshooting", "help/troubleshooting"),
    ("overview", "concepts"),
    ("deploy", "operate/deploy"),
    ("maintain", "operate/maintain"),
    ("migrate", "operate/migrate"),
    ("security", "operate/security"),
    ("test", "operate/test"),
    ("tutorial", "develop/tutorials"),
    ("faqs", "help/faqs"),
]
FORWARD_FILES = [("glossary.md", "concepts/glossary.md")]


def reverse_remap(rel: str) -> str:
    """new path → old path."""
    if rel == "concepts/glossary.md":
        return "glossary.md"
    for new, old in REVERSE:
        if rel == new:
            return old
        if rel.startswith(new + "/"):
            return old + rel[len(new):]
    return rel


def forward_remap(rel: str) -> str:
    for old, new in FORWARD_FILES:
        if rel == old:
            return new
    for old, new in FORWARD:
        if rel == old:
            return new
        if rel.startswith(old + "/"):
            return new + rel[len(old):]
    return rel


LINK_RE = re.compile(r'(\[[^\]]*\])\(([^)\s]+)(\s+"[^"]*")?\)')

EXTERNAL_PREFIXES = (
    "http://", "https://", "mailto:", "tel:", "ftp://", "ftps://",
    "javascript:", "data:", "#",
)


def fix_link(lang_dir: Path, new_src_rel: str, link: str) -> str:
    """new_src_rel:文件目前(新)路径,相对 source/<lang>/。
    link:括号内的 url。
    返回新 link 或原值。
    """
    if link.startswith(EXTERNAL_PREFIXES):
        return link
    if link.startswith("/"):
        return link

    if "#" in link:
        path_part, anchor = link.split("#", 1)
        anchor = "#" + anchor
    else:
        path_part = link
        anchor = ""

    if not path_part:
        return link

    new_src_dir = os.path.dirname(new_src_rel)

    # 1) 试用 NEW 形式 resolve
    target_via_new = os.path.normpath(os.path.join(new_src_dir, path_part)).replace("\\", "/")
    if not target_via_new.startswith(".."):
        # 检查目标是否存在(.md 或目录或图片)
        target_path = lang_dir / target_via_new
        if target_path.exists():
            return link  # 已是 NEW 形式

    # 2) 试用 OLD 形式 resolve(即把当前 link 当作旧位置下的相对路径)
    old_src_rel = reverse_remap(new_src_rel)
    old_src_dir = os.path.dirname(old_src_rel)
    target_via_old = os.path.normpath(os.path.join(old_src_dir, path_part)).replace("\\", "/")
    if target_via_old.startswith(".."):
        return link

    # 这个 old target 在新结构里的位置
    new_target = forward_remap(target_via_old)
    new_target_path = lang_dir / new_target
    if not new_target_path.exists():
        # 目标也不在新位置,可能是断链(原本就坏)。保持原值。
        return link

    new_rel = os.path.relpath(new_target, new_src_dir).replace("\\", "/")
    return new_rel + anchor


def process(lang_dir: Path) -> int:
    total = 0
    files_changed = 0
    for path in sorted(lang_dir.rglob("*.md")):
        rel = path.relative_to(lang_dir).as_posix()
        original = path.read_text(encoding="utf-8")
        changes = 0

        def sub(m):
            nonlocal changes
            text, link, title = m.group(1), m.group(2), m.group(3) or ""
            new_link = fix_link(lang_dir, rel, link)
            if new_link != link:
                changes += 1
            return f"{text}({new_link}{title})"

        new_content = LINK_RE.sub(sub, original)
        if changes:
            path.write_text(new_content, encoding="utf-8")
            files_changed += 1
            total += changes
    return files_changed, total


def main():
    for lang in LANGS:
        lang_dir = SOURCE / lang
        if not lang_dir.exists():
            continue
        print(f"== {lang}")
        f, t = process(lang_dir)
        print(f"  改了 {f} 个文件,共 {t} 处链接")


if __name__ == "__main__":
    main()
