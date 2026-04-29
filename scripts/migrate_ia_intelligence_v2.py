#!/usr/bin/env python3
"""IA v2 重构:matrixone-intelligence(zh + en)从 v1(9 一级)→ v2(9 一级,但重新分类)。

v2 IA:
  1. get-started/        (不变)
  2. overview/           (瘦身,只剩产品介绍/兼容性/MO 助手)
  3. genai-workspace/    (吃 v1 workspace/management + data 整体)
  4. database-instance/  (吃 v1 workspace/instance + workspace/db-instance.md + operate 整体)
  5. develop/            (不变)
  6. billing/            (NEW 独立一级,从 v1 overview/charging + overview/billing.md 抽出)
  7. reference/          (不变)
  8. help/               (吃 v1 overview/protocols + overview/protocol)
  9. release-notes/      (不变)

跑 zh 和 en 两遍。
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "matrixone-intelligence" / "source"
LANGS = ["zh", "en"]

# 顺序:更长 / 更具体 prefix 先(避免 workspace/management 命中 workspace 先)
DIR_MOVES = [
    # GenAI Workspace 收 data + workspace/management
    ("data/connect",                "genai-workspace/connect"),
    ("data/explore",                "genai-workspace/explore"),
    ("data/processing",             "genai-workspace/processing"),
    ("data/sharing",                "genai-workspace/sharing"),
    ("data/migrate",                "genai-workspace/migrate"),
    ("workspace/management",        "genai-workspace/management"),

    # Database Instance 收 workspace/instance + operate
    ("workspace/instance",          "database-instance/instance"),
    ("operate/alarm",               "database-instance/alarm"),
    ("operate/backup-restore",      "database-instance/backup-restore"),
    ("operate/events",              "database-instance/events"),
    ("operate/monitor",             "database-instance/monitor"),
    ("operate/security",            "database-instance/security"),

    # Billing 独立
    ("overview/charging",           "billing"),

    # Protocols 进 help/legal
    ("overview/protocol",           "help/legal"),
]

FILE_MOVES = [
    # billing.md(原 overview/billing.md 是 charging 的 wrapper)→ billing/index.md
    ("overview/billing.md",         "billing/index_old_wrapper.md"),

    # protocols.md(原 overview/protocols.md 是 protocol/ 的 wrapper)→ help/legal/index.md
    ("overview/protocols.md",       "help/legal/index_old_wrapper.md"),
]

# 旧的 wrapper / index 文件,迁完后要 rm,因为新 section index 会重写
TO_DELETE_AFTER = [
    "data/index.md",
    "workspace/index.md",
    "workspace/genai-workspace.md",
    "workspace/db-instance.md",
    "operate/index.md",
    "billing/index_old_wrapper.md",
    "help/legal/index_old_wrapper.md",
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
        # 试加 .md 看是否是 file move
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
    # 未跟踪 → 退回到 shutil.move + git add 让 git 自己识别
    import shutil
    src_p = cwd / src
    dst_p = cwd / dst
    if dst_p.exists():
        try:
            dst_p.rmdir()  # 空目录可删
        except OSError:
            pass
    shutil.move(str(src_p), str(dst_p))
    run("git", "add", "-A", dst, cwd=cwd, check=False)


def physical_move(lang_dir: Path):
    def exists(p: str) -> bool:
        return (lang_dir / p).exists()

    # 1) 建新父目录
    for d in ["genai-workspace", "database-instance", "billing", "help/legal"]:
        (lang_dir / d).mkdir(parents=True, exist_ok=True)

    # 2) DIR_MOVES
    for old, new in DIR_MOVES:
        if not exists(old):
            continue
        if not exists(new):
            git_mv(old, new, cwd=lang_dir)
            continue
        # 目标存在(可能我们刚 mkdir 是空的)→ rmdir 后 mv
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

    # 3) FILE_MOVES
    for old, new in FILE_MOVES:
        if exists(old):
            git_mv(old, new, cwd=lang_dir)

    # 4) 删空目录(原 data/, workspace/, operate/ 应该已经空了)
    for d in ["data", "workspace", "operate"]:
        p = lang_dir / d
        if p.exists():
            try:
                # 递归删空子目录
                for sub in sorted(p.rglob("*"), reverse=True):
                    if sub.is_dir():
                        try:
                            sub.rmdir()
                        except OSError:
                            pass
                p.rmdir()
            except OSError:
                pass

    # 5) 删旧 wrapper / index(可能 tracked 也可能只在 working tree)
    for f in TO_DELETE_AFTER:
        p = lang_dir / f
        if not p.exists():
            continue
        # 试 git rm --ignore-unmatch,失败就 fall back 到 unlink
        r = run("git", "rm", "-f", "--ignore-unmatch", f, cwd=lang_dir, check=False)
        if p.exists():
            p.unlink()

    # 6) 再清一遍 data/ workspace/ operate/(刚才 unlink 完里面的 index.md 后可能空了)
    for d in ["data", "workspace", "operate"]:
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
