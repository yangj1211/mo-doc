#!/usr/bin/env python3
"""IA 重构:matrixone 站从 16 顶级目录改成 7 一级。

| 旧                       | 新                       |
|--------------------------|--------------------------|
| overview/                | concepts/                |
| glossary.md              | concepts/glossary.md     |
| getting-started/         | get-started/             |
| deploy/                  | operate/deploy/          |
| maintain/                | operate/maintain/        |
| migrate/                 | operate/migrate/         |
| performance-tuning/      | operate/performance/     |
| security/                | operate/security/        |
| test/                    | operate/test/            |
| sql-reference/           | reference/               |
| troubleshooting/         | help/troubleshooting/    |
| faqs/                    | help/faqs/               |
| tutorial/                | develop/tutorials/       |

contribution-guide/ 保留原位(不进顶 nav,后续放页脚)。

跑两遍:zh 一遍,en 一遍。先全量重写 .md 内的相对链接 + toctree 引用,
再 git mv 物理移动。

EN 站 concepts/ 已经存在(只有 data-branch.md);overview→concepts 时
按文件级 mv 合并,不覆盖。
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SOURCE = REPO / "matrixone" / "source"
LANGS = ["zh", "en"]

# 顺序:更长 / 更具体的 prefix 先,避免 "test" 命中 "tests"
DIR_MOVES = [
    ("performance-tuning", "operate/performance"),
    ("getting-started", "get-started"),
    ("sql-reference", "reference"),
    ("troubleshooting", "help/troubleshooting"),
    ("contribution-guide", "contribution-guide"),  # noop,占位防 prefix 误命中
    ("overview", "concepts"),
    ("deploy", "operate/deploy"),
    ("maintain", "operate/maintain"),
    ("migrate", "operate/migrate"),
    ("security", "operate/security"),
    ("test", "operate/test"),
    ("tutorial", "develop/tutorials"),
    ("faqs", "help/faqs"),
]

FILE_MOVES = [
    ("glossary.md", "concepts/glossary.md"),
]


def remap_path(rel: str) -> str:
    """rel 是相对 source/<lang>/ 的 POSIX 路径。"""
    rel = rel.replace("\\", "/")
    if rel == "":
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


# Markdown link `[text](url)`,支持 url 内含空格转义、不含右括号
LINK_RE = re.compile(r'(\[(?:[^\]\n]*)\])\(([^)\s]+)(\s+"[^"]*")?\)')

# Toctree:解析 ```{toctree} ... ``` 块体
TOCTREE_OPEN_RE = re.compile(r'^\s*```{toctree}')
FENCE_RE = re.compile(r'^\s*```')

EXTERNAL_PREFIXES = (
    "http://", "https://", "mailto:", "tel:", "ftp://", "ftps://",
    "javascript:", "data:", "#",
)


def update_link(src_rel: str, link: str) -> str:
    """src_rel:文件原(旧)路径,相对 source/<lang>/。
    link:markdown link 内括号里那串。
    返回新 link(可能保持原样)。
    """
    if link.startswith(EXTERNAL_PREFIXES):
        return link
    if link.startswith("/"):  # 站内绝对(罕见,留给作者意图)
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

    # 跨出 source/<lang>/ 的不动
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
    """toctree 里的 doc 引用(无扩展名)。可以是相对当前 index.md 的目录,
    也可以是 source-root 绝对(以 / 开头)。"""
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
    new_rel = os.path.relpath(new_target, new_src_dir).replace("\\", "/")
    return new_rel


def process_md(path: Path, src_rel: str) -> int:
    """改写 .md 文件里的相对链接 + toctree。返回 changes 数。"""
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

    # toctree 块
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
            # 空行 / 选项行 / self 跳过
            if (not stripped or stripped.startswith(":") or stripped == "self"):
                out_lines.append(line)
                continue

            indent = line[: len(line) - len(line.lstrip())]
            # 形式 1:Title <doc/path>
            m = re.match(r"^(.+?<)([^>]+)(>.*)$", stripped)
            if m:
                pre, doc, post = m.group(1), m.group(2), m.group(3)
                new_doc = update_doc_ref(src_rel, doc)
                if new_doc != doc:
                    changes += 1
                out_lines.append(f"{indent}{pre}{new_doc}{post}")
                continue
            # 形式 2:bare doc path
            new_doc = update_doc_ref(src_rel, stripped)
            if new_doc != stripped:
                changes += 1
                out_lines.append(f"{indent}{new_doc}")
            else:
                out_lines.append(line)
            continue

        out_lines.append(line)

    new_content = "\n".join(out_lines)
    # 必须对照 original(读入时的原文),不是 content(已经被 LINK_RE.sub 改过的中间值);
    # 否则只改了 link 没改 toctree 的文件会被错误地判为"未变化"而不写回。
    if new_content != original:
        path.write_text(new_content, encoding="utf-8")
    return changes


def rewrite_links(lang_dir: Path) -> tuple[int, int]:
    """对 lang_dir 下所有 .md 改写,返回 (file_count_changed, total_changes)."""
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
    """thin git wrapper"""
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
    """git mv,允许目标父目录不存在(自动 mkdir)。"""
    Path(cwd / dst).parent.mkdir(parents=True, exist_ok=True)
    run("git", "mv", src, dst, cwd=cwd)


def physical_move(lang_dir: Path):
    """git mv 旧目录/文件到新位置。"""

    def exists(p: str) -> bool:
        return (lang_dir / p).exists()

    # 1) 先建新父目录(空 dir 不会被 git 跟踪,后面 mv 时自动跟踪文件)
    for d in ["operate", "help", "develop/tutorials"]:
        (lang_dir / d).mkdir(parents=True, exist_ok=True)

    # 2) overview → concepts(en 已存在 concepts/data-branch.md,文件级合并)
    if exists("overview"):
        if exists("concepts") and any((lang_dir / "concepts").iterdir()):
            for item in sorted((lang_dir / "overview").iterdir()):
                target_rel = f"concepts/{item.name}"
                if exists(target_rel):
                    print(f"  ⚠ 冲突跳过:overview/{item.name} → {target_rel}")
                    continue
                git_mv(f"overview/{item.name}", target_rel, cwd=lang_dir)
            try:
                (lang_dir / "overview").rmdir()
            except OSError:
                print(f"  ⚠ overview/ 非空,保留")
        else:
            # 无冲突,整体 mv;但要先确保 concepts/ 不是空目录(rmdir 之)
            if exists("concepts"):
                try:
                    (lang_dir / "concepts").rmdir()
                except OSError:
                    pass
            git_mv("overview", "concepts", cwd=lang_dir)

    # 3) glossary.md → concepts/glossary.md
    if exists("glossary.md"):
        git_mv("glossary.md", "concepts/glossary.md", cwd=lang_dir)

    # 4) getting-started → get-started
    if exists("getting-started"):
        git_mv("getting-started", "get-started", cwd=lang_dir)

    # 5) deploy/maintain/migrate/security/test → operate/*
    for d in ["deploy", "maintain", "migrate", "security", "test"]:
        if exists(d):
            git_mv(d, f"operate/{d}", cwd=lang_dir)
    if exists("performance-tuning"):
        git_mv("performance-tuning", "operate/performance", cwd=lang_dir)

    # 6) sql-reference → reference
    if exists("sql-reference"):
        git_mv("sql-reference", "reference", cwd=lang_dir)

    # 7) troubleshooting → help/troubleshooting,faqs → help/faqs
    for d in ["troubleshooting", "faqs"]:
        if exists(d):
            git_mv(d, f"help/{d}", cwd=lang_dir)

    # 8) tutorial/* → develop/tutorials/*(逐个文件 mv,因为目标父 dir 已存在)
    if exists("tutorial"):
        for item in sorted((lang_dir / "tutorial").iterdir()):
            git_mv(f"tutorial/{item.name}", f"develop/tutorials/{item.name}", cwd=lang_dir)
        try:
            (lang_dir / "tutorial").rmdir()
        except OSError:
            print("  ⚠ tutorial/ 非空,保留")


def main():
    for lang in LANGS:
        lang_dir = SOURCE / lang
        if not lang_dir.exists():
            print(f"== skip {lang}(目录不存在)")
            continue
        print(f"\n== {lang}")
        print("  步骤 1:改写 .md 链接 + toctree")
        files, total = rewrite_links(lang_dir)
        print(f"    改了 {files} 个文件,共 {total} 处链接")
        print("  步骤 2:git mv 物理移动")
        physical_move(lang_dir)
    print("\n完成。请跑 `make html` 看 warning。")


if __name__ == "__main__":
    main()
