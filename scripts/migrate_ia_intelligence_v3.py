#!/usr/bin/env python3
"""IA v3:matrixone-intelligence(zh + en)从 v2(9 一级)→ v3(8 一级)。

v3:数据库实例和工作区合并成一个统一"工作区"入口,develop/app-develop 主体
吸收成 workspace/sql + workspace/instance/drivers。

v3 IA:
  1. get-started/    (不变)
  2. overview/       (不变)
  3. workspace/      (NEW 统一)
       ├─ management/  (← genai-workspace/management)
       ├─ instance/    (← database-instance/instance,新增 drivers/)
       ├─ data/        (← genai-workspace/{connect,explore,processing,sharing,migrate})
       ├─ sql/         (NEW: ← develop/app-develop/{schema-design,import-data,read-data,Transactions,Tutorial})
       ├─ ops/         (← database-instance/{monitor,alarm,events,backup-restore,security})
       └─ tools/       (← develop/app-develop/export-data/modump)
  4. develop/        (瘦:workflow-api / mcp / deerflow)
  5. billing/        (不变)
  6. reference/      (不变)
  7. help/           (不变)
  8. release-notes/  (不变)
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "matrixone-intelligence" / "source"
LANGS = ["zh", "en"]

# 顺序:更长 / 更具体 prefix 先
DIR_MOVES = [
    # database-instance → workspace
    ("database-instance/instance",            "workspace/instance"),
    ("database-instance/monitor",             "workspace/ops/monitor"),
    ("database-instance/alarm",               "workspace/ops/alarm"),
    ("database-instance/events",              "workspace/ops/events"),
    ("database-instance/backup-restore",      "workspace/ops/backup-restore"),
    ("database-instance/security",            "workspace/ops/security"),

    # genai-workspace → workspace
    ("genai-workspace/management",            "workspace/management"),
    ("genai-workspace/connect",               "workspace/data/connect"),
    ("genai-workspace/explore",               "workspace/data/explore"),
    ("genai-workspace/processing",            "workspace/data/processing"),
    ("genai-workspace/sharing",               "workspace/data/sharing"),
    ("genai-workspace/migrate",               "workspace/data/migrate"),

    # develop/app-develop → workspace/sql
    ("develop/app-develop/schema-design",     "workspace/sql/schema-design"),
    ("develop/app-develop/import-data",       "workspace/sql/data-rw/import-data"),
    ("develop/app-develop/read-data",         "workspace/sql/data-rw/read-data"),
    ("develop/app-develop/Transactions",      "workspace/sql/transactions"),
    ("develop/app-develop/Tutorial",          "workspace/sql/tutorial"),
]

# 单文件移动(顺便重命名 connect-mo 7 个驱动 + modump)
FILE_MOVES = [
    ("develop/app-develop/connect-mo/database-client-tools.md",
     "workspace/instance/drivers/client-tools.md"),
    ("develop/app-develop/connect-mo/connect-mo-with-web.md",
     "workspace/instance/drivers/web-client.md"),
    ("develop/app-develop/connect-mo/java-connect-to-matrixone/connect-mo-with-jdbc.md",
     "workspace/instance/drivers/jdbc.md"),
    ("develop/app-develop/connect-mo/java-connect-to-matrixone/connect-mo-with-orm.md",
     "workspace/instance/drivers/orm.md"),
    ("develop/app-develop/connect-mo/python-connect-to-matrixone.md",
     "workspace/instance/drivers/python.md"),
    ("develop/app-develop/connect-mo/connect-to-matrixone-with-go.md",
     "workspace/instance/drivers/go.md"),
    ("develop/app-develop/connect-mo/connect-to-matrixone-with-c#.md",
     "workspace/instance/drivers/csharp.md"),
    ("develop/app-develop/export-data/modump.md",
     "workspace/tools/modump.md"),
]

TO_DELETE_AFTER = [
    "database-instance/index.md",
    "genai-workspace/index.md",
]


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
    if new_target == old_target:
        new_with_md = remap_path(old_target + ".md")
        if new_with_md != old_target + ".md" and new_with_md.endswith(".md"):
            new_target = new_with_md[:-3]
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
    r = subprocess.run(list(args), cwd=str(cwd) if cwd else None,
                       capture_output=True, text=True)
    if check and r.returncode != 0:
        sys.stderr.write(f"FAIL: {' '.join(args)}\n{r.stderr}\n")
        sys.exit(1)
    return r


def git_mv(src: str, dst: str, cwd: Path):
    Path(cwd / dst).parent.mkdir(parents=True, exist_ok=True)
    r = run("git", "mv", src, dst, cwd=cwd, check=False)
    if r.returncode == 0:
        return
    src_p = cwd / src
    dst_p = cwd / dst
    if dst_p.exists():
        try:
            dst_p.rmdir()
        except OSError:
            pass
    shutil.move(str(src_p), str(dst_p))
    run("git", "add", "-A", dst, cwd=cwd, check=False)


def physical_move(lang_dir: Path):
    def exists(p: str) -> bool:
        return (lang_dir / p).exists()

    # 1) 建新父目录
    for d in ["workspace/management", "workspace/instance", "workspace/instance/drivers",
              "workspace/data", "workspace/sql/data-rw", "workspace/ops",
              "workspace/tools"]:
        (lang_dir / d).mkdir(parents=True, exist_ok=True)

    # 2) FILE_MOVES 先(避免 connect-mo 整目录 dir-move 后再做单文件操作)
    for old, new in FILE_MOVES:
        if not exists(old):
            continue
        git_mv(old, new, cwd=lang_dir)

    # 3) DIR_MOVES
    for old, new in DIR_MOVES:
        if not exists(old):
            continue
        if not exists(new):
            git_mv(old, new, cwd=lang_dir)
            continue
        try:
            (lang_dir / new).rmdir()
            git_mv(old, new, cwd=lang_dir)
        except OSError:
            for item in sorted((lang_dir / old).iterdir()):
                tgt = f"{new}/{item.name}"
                if exists(tgt):
                    print(f"  ⚠ 冲突跳过:{old}/{item.name} → {tgt}")
                    continue
                git_mv(f"{old}/{item.name}", tgt, cwd=lang_dir)
            try:
                (lang_dir / old).rmdir()
            except OSError:
                pass

    # 4) 清理空旧目录
    for d in ["database-instance", "genai-workspace", "develop/app-develop"]:
        p = lang_dir / d
        if not p.exists():
            continue
        try:
            for sub in sorted(p.rglob("*"), reverse=True):
                if sub.is_dir():
                    try:
                        sub.rmdir()
                    except OSError:
                        pass
            p.rmdir()
        except OSError:
            pass

    # 5) 删旧 wrapper / index
    for f in TO_DELETE_AFTER:
        p = lang_dir / f
        if not p.exists():
            continue
        run("git", "rm", "-f", "--ignore-unmatch", f, cwd=lang_dir, check=False)
        if p.exists():
            p.unlink()


def main():
    for lang in LANGS:
        lang_dir = SOURCE / lang
        if not lang_dir.exists():
            continue
        print(f"\n== matrixone-intelligence/{lang}")
        print("  步骤 1:改写 .md 链接 + toctree")
        files, total = rewrite_links(lang_dir)
        print(f"    改了 {files} 个文件,共 {total} 处链接")
        print("  步骤 2:git mv 物理移动")
        physical_move(lang_dir)
    print("\n完成。")


if __name__ == "__main__":
    main()
