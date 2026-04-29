#!/usr/bin/env python3
"""IA 重构:matrixone-intelligence 站(zh-only)从 34 顶级混合(CamelCase + lowercase + 散文件)
改成 9 一级 lowercase。EN 当前 5 篇,先不动(用户:"en 先不管了")。

新 IA(9 一级,与 matrixone 错开,因为 intelligence 是 AI 数据平台):
  1. get-started/   快速开始
  2. overview/      产品概览(含 intro / billing / protocol)
  3. workspace/     工作空间(含 instance / mgmt / genai-workspace)
  4. data/          数据(connect / explore / processing / sharing / migrate)
  5. develop/       开发与 API(app-develop / mcp / workflow-api / deerflow)
  6. operate/       运维(alarm / monitor / events / backup-restore / security)
  7. reference/     参考
  8. help/          帮助(faqs / tech-support / glossary)
  9. release-notes/ 版本发布

注意:
- macOS APFS 默认 case-insensitive,case-only rename(如 Overview → overview)
  必须走中转名,否则 git mv 是 no-op。
- 同一目标父 dir 已存在(如 Overview 也叫 overview)的情况:文件级合并。
- 11 个根 .md 散文件(intro / start / billing / protocols / monitoring 等)分发到对应一级。
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "matrixone-intelligence" / "source"
LANG_DIR = SOURCE / "zh"

# 顺序:更长 prefix 优先(避免 "Data-Sharing" 误命中 "Data")
DIR_MOVES = [
    ("Workspace-Mgmt",   "workspace/management"),
    ("Instance-Mgmt",    "workspace/instance"),
    ("Backup-Restore",   "operate/backup-restore"),
    ("Migrate-Data",     "data/migrate"),
    ("Data-Connect",     "data/connect"),
    ("Data-Explore",     "data/explore"),
    ("Data-Processing",  "data/processing"),
    ("Data-Sharing",     "data/sharing"),
    ("Get-Started",      "get-started"),
    ("Release-Notes",    "release-notes"),
    ("App-Develop",      "develop/app-develop"),
    ("Reference",        "reference"),
    ("Overview",         "overview"),
    ("Charging",         "overview/charging"),
    ("Protocol",         "overview/protocol"),
    ("Security",         "operate/security"),
    ("Monitor",          "operate/monitor"),
    ("Events",           "operate/events"),
    ("Alarm",            "operate/alarm"),
    ("FAQs",             "help/faqs"),
    ("workflow-api",     "develop/workflow-api"),
    ("mcp",              "develop/mcp"),
    # develop/ 已存在,deerflow.md 在里面,不需要 mv 顶级 develop 目录本身
    # 但 develop/deerflow.md 这种文件需要保持原位 → 在 FILE_MOVES 里不列即可。
]

FILE_MOVES = [
    ("intro.md",            "overview/intro.md"),
    ("start.md",            "get-started/start.md"),
    ("billing.md",          "overview/billing.md"),
    ("protocols.md",        "overview/protocols.md"),
    ("genai-workspace.md",  "workspace/genai-workspace.md"),
    ("db-instance.md",      "workspace/db-instance.md"),
    ("monitoring.md",       "operate/monitoring.md"),
    ("releases.md",         "release-notes/releases.md"),
    ("tech-support.md",     "help/tech-support.md"),
    ("glossary.md",         "help/glossary.md"),
]

# 已经在新位置的 lowercase 目录(不动,但记录避免误命中)
ALREADY_LOWERCASE = ["develop"]


def remap_path(rel: str) -> str:
    rel = rel.replace("\\", "/")
    if not rel:
        return rel
    for old, new in FILE_MOVES:
        if rel == old:
            return new
    for old, new in DIR_MOVES:
        if rel == old:
            return new
        if rel.startswith(old + "/"):
            return new + rel[len(old):]
    return rel


LINK_RE = re.compile(r'(\[[^\]]*\])\(([^)\s]+)(\s+"[^"]*")?\)')
TOCTREE_OPEN_RE = re.compile(r'^\s*```{toctree}')
FENCE_RE = re.compile(r'^\s*```')

EXTERNAL_PREFIXES = (
    "http://", "https://", "mailto:", "tel:", "ftp://", "ftps://",
    "javascript:", "data:", "#",
)


def update_link(src_rel: str, link: str) -> str:
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

    src_dir = os.path.dirname(src_rel)
    old_target = os.path.normpath(os.path.join(src_dir, path_part)).replace("\\", "/")
    if old_target.startswith("..") or old_target == ".":
        return link

    new_target = remap_path(old_target)
    new_src = remap_path(src_rel)
    new_src_dir = os.path.dirname(new_src)

    new_rel = os.path.relpath(new_target, new_src_dir).replace("\\", "/")
    if new_rel == ".":
        new_rel = ""
    return new_rel + anchor


def update_doc_ref(src_rel: str, doc: str) -> str:
    if doc == "self" or not doc:
        return doc
    src_dir = os.path.dirname(src_rel)
    if doc.startswith("/"):
        old_target = doc.lstrip("/")
    else:
        old_target = os.path.normpath(os.path.join(src_dir, doc)).replace("\\", "/")
    if old_target.startswith("..") or old_target == ".":
        return doc

    new_target = remap_path(old_target)
    new_src = remap_path(src_rel)
    new_src_dir = os.path.dirname(new_src)

    if doc.startswith("/"):
        return "/" + new_target
    return os.path.relpath(new_target, new_src_dir).replace("\\", "/")


def process_md(path: Path, src_rel: str) -> int:
    original = path.read_text(encoding="utf-8")
    content = original
    changes = 0

    def sub_link(m):
        nonlocal changes
        text, link, title = m.group(1), m.group(2), m.group(3) or ""
        new_link = update_link(src_rel, link)
        if new_link != link:
            changes += 1
        return f"{text}({new_link}{title})"

    content = LINK_RE.sub(sub_link, content)

    out_lines = []
    in_toctree = False
    for line in content.split("\n"):
        if not in_toctree and TOCTREE_OPEN_RE.match(line):
            in_toctree = True
            out_lines.append(line)
            continue
        if in_toctree and FENCE_RE.match(line) and "{toctree}" not in line:
            in_toctree = False
            out_lines.append(line)
            continue
        if in_toctree:
            stripped = line.strip()
            if not stripped or stripped.startswith(":") or stripped == "self":
                out_lines.append(line)
                continue
            indent = line[: len(line) - len(line.lstrip())]
            m = re.match(r"^(.+?<)([^>]+)(>.*)$", stripped)
            if m:
                pre, doc, post = m.group(1), m.group(2), m.group(3)
                new_doc = update_doc_ref(src_rel, doc)
                if new_doc != doc:
                    changes += 1
                out_lines.append(f"{indent}{pre}{new_doc}{post}")
                continue
            new_doc = update_doc_ref(src_rel, stripped)
            if new_doc != stripped:
                changes += 1
                out_lines.append(f"{indent}{new_doc}")
            else:
                out_lines.append(line)
            continue
        out_lines.append(line)

    new_content = "\n".join(out_lines)
    if new_content != original:
        path.write_text(new_content, encoding="utf-8")
    return changes


def rewrite_links(lang_dir: Path) -> tuple[int, int]:
    files_changed = 0
    total = 0
    for path in sorted(lang_dir.rglob("*.md")):
        rel = path.relative_to(lang_dir).as_posix()
        n = process_md(path, rel)
        if n:
            files_changed += 1
            total += n
    return files_changed, total


def run(*args, cwd: Path | None = None, check: bool = True):
    r = subprocess.run(
        list(args),
        cwd=str(cwd) if cwd else None,
        capture_output=True,
        text=True,
    )
    if check and r.returncode != 0:
        sys.stderr.write(f"FAIL: {' '.join(args)}\n{r.stderr}\n")
        sys.exit(1)
    return r


def git_mv(src: str, dst: str, cwd: Path):
    Path(cwd / dst).parent.mkdir(parents=True, exist_ok=True)
    run("git", "mv", src, dst, cwd=cwd)


def case_insensitive_dir_rename(old: str, new: str, cwd: Path):
    """Old/new 只是大小写差(APFS case-insensitive),走中转名。
    Old/new 也可能是不同名(如 Overview → overview),先 mv 到 _tmp_ 再 mv 到新名。"""
    if (cwd / old) == (cwd / new):
        # 严格相同
        return
    tmp = old + "__migrate_tmp__"
    git_mv(old, tmp, cwd=cwd)
    git_mv(tmp, new, cwd=cwd)


def physical_move(lang_dir: Path):
    def exists(p: str) -> bool:
        return (lang_dir / p).exists()

    # 1) 先建新父目录
    for d in ["overview", "workspace", "data", "operate", "help",
              "get-started", "reference", "release-notes",
              "develop"]:
        (lang_dir / d).mkdir(parents=True, exist_ok=True)

    # 2) 处理 DIR_MOVES。注意 case-only rename 走中转
    for old, new in DIR_MOVES:
        if not exists(old):
            continue
        # 同名(case-insensitive)的纯换大小写
        if old.lower() == new.lower() and "/" not in new:
            case_insensitive_dir_rename(old, new, cwd=lang_dir)
            continue
        # 目标不存在 → 直接 mv
        if not exists(new):
            # 但目标父 dir 上面已 mkdir,父 dir 存在但目标本身不存在 → OK
            # APFS:如果 new 名字 case-insensitive 撞了已存在的 OLD(刚才 mkdir 创了空 new),
            # mkdir 在 APFS 上对 "overview" 和 "Overview" 视为同一,所以不会真创建第二个。
            # 实际:如果 lower(new) == lower(old) 且只是大小写差,mkdir 不会建,exists(new) 仍 True。
            # 这种情况进 case-only 分支。已处理。
            git_mv(old, new, cwd=lang_dir)
            continue
        # 目标存在(我们刚 mkdir,通常是空的) → rmdir 目标后 mv
        try:
            (lang_dir / new).rmdir()  # 空就能 rm
            git_mv(old, new, cwd=lang_dir)
        except OSError:
            # 非空,做文件级合并
            for item in sorted((lang_dir / old).iterdir()):
                target = f"{new}/{item.name}"
                if exists(target):
                    print(f"  ⚠ 冲突跳过:{old}/{item.name} → {target}")
                    continue
                git_mv(f"{old}/{item.name}", target, cwd=lang_dir)
            try:
                (lang_dir / old).rmdir()
            except OSError:
                pass

    # 3) 文件级 mv
    for old, new in FILE_MOVES:
        if exists(old):
            git_mv(old, new, cwd=lang_dir)


def main():
    print(f"== matrixone-intelligence/zh")
    print("  步骤 1:改写 .md 链接 + toctree")
    files, total = rewrite_links(LANG_DIR)
    print(f"    改了 {files} 个文件,共 {total} 处链接")
    print("  步骤 2:git mv 物理移动")
    physical_move(LANG_DIR)
    print("\n完成。")


if __name__ == "__main__":
    main()
