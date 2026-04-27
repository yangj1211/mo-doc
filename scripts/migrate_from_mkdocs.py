#!/usr/bin/env python3
"""
将 matrixorigin.io.cn (mkdocs) 的全部文档批量迁移到本 demo 项目（Sphinx）。

输入：
  - /Users/admin/project/moi/official_website/matrixorigin.io.cn/mkdocs.yml
    （nav 部分作为唯一权威结构来源）
  - /Users/admin/project/moi/official_website/matrixorigin.io.cn/docs/

输出：
  - /Users/admin/project/moi/docs-demo/matrixone/<section>/...   (中文)
  - 每个 section 根下生成 index.md，按 mkdocs nav 的分组生成 toctree
  - 把整个 docs/MatrixOne/images 拷过来，相对路径还能 resolve
"""
import sys
import shutil
from pathlib import Path
import yaml

SRC_REPO = Path('/Users/admin/project/moi/official_website/matrixorigin.io.cn')
MKDOCS_YML = SRC_REPO / 'mkdocs.yml'
SRC_DOCS = SRC_REPO / 'docs'

DST_ROOT = Path('/Users/admin/project/moi/docs-demo/matrixone')

# nav 顶层中文分组 → 目标目录
SECTION_DIR = {
    '关于 MatrixOne': 'overview',
    '快速开始': 'getting-started',
    '开发指南': 'develop',
    '部署指南': 'deploy',
    '运维': 'maintain',
    '数据迁移': 'migrate',
    '测试': 'test',
    '性能调优': 'performance-tuning',
    '安全与权限': 'security',
    '参考手册': 'sql-reference',
    '故障诊断': 'troubleshooting',
    '常见问题解答': 'faqs',
    '版本发布纪要': 'release-notes',
    '社区贡献指南': 'contribution-guide',
}

# 源 MatrixOne/<X>/... → 目标 <Y>/...（X / Y 是顶级目录名映射）
PATH_REMAP = {
    'Overview': 'overview',
    'Get-Started': 'getting-started',
    'Develop': 'develop',
    'Deploy': 'deploy',
    'Maintain': 'maintain',
    'Migrate': 'migrate',
    'Test': 'test',
    'Performance-Tuning': 'performance-tuning',
    'Security': 'security',
    'Reference': 'sql-reference',
    'Troubleshooting': 'troubleshooting',
    'FAQs': 'faqs',
    'Release-Notes': 'release-notes',
    'Contribution-Guide': 'contribution-guide',
    'Tutorial': 'tutorial',          # 没有独立 nav 顶层项，但被 Develop 引用
}


def remap_md_path(src_path: str) -> Path:
    """
    'MatrixOne/Overview/feature/foo.md' → Path('overview/feature/foo.md')
    'MatrixOne/glossary.md'             → Path('glossary.md')
    'README.md'                         → Path('index.md')
    顶级目录用 PATH_REMAP；其余 dir 部分一律小写，文件名保持原样。
    """
    if src_path == 'README.md':
        return Path('index.md')
    parts = src_path.split('/')
    if parts[0] != 'MatrixOne':
        # 应当不会出现，但保险起见原样落地
        return Path(*parts)
    if len(parts) == 2:                 # MatrixOne/glossary.md
        return Path(parts[1])
    section = parts[1]
    section_dir = PATH_REMAP.get(section, section.lower())
    *mid, fname = parts[2:]
    mid = [d.lower() for d in mid]
    return Path(section_dir, *mid, fname)


def copy_one(src_md: str) -> Path | None:
    """拷一个 .md，返回目标相对路径（相对 source/）。"""
    src = SRC_DOCS / src_md
    if not src.exists():
        print(f"  ! missing: {src_md}", file=sys.stderr)
        return None
    rel = remap_md_path(src_md)
    dst = DST_ROOT / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return rel


def walk_section(items, copied: list[tuple[str, Path]]):
    """
    递归遍历某个 section 子树。返回该层级的 [(label, target_relpath_or_subgroup), ...]，
    以便上层组装 toctree。同时把所有遇到的 .md 拷贝到目标位置。

    每个 nav item 是 dict {label: value}，value 要么是字符串（.md 路径），
    要么是 list（子分组）。
    """
    out = []
    for item in items:
        assert isinstance(item, dict) and len(item) == 1
        label, value = next(iter(item.items()))
        if isinstance(value, str):
            # leaf
            rel = copy_one(value)
            if rel is not None:
                out.append((label, rel))
                copied.append((value, rel))
        elif isinstance(value, list):
            # group
            sub = walk_section(value, copied)
            out.append((label, sub))
        else:
            print(f"  ? skipped: {label} = {value!r}", file=sys.stderr)
    return out


def relpath_for_toctree(target_rel: Path, section_dir: Path) -> str:
    """
    生成 toctree 里的引用：去掉 .md 扩展名，相对 section 根。
    支持跨 section 引用（比如 Develop 里嵌入了 Tutorial/* 文章），用 ../ 形式。
    """
    import os
    rel = os.path.relpath(target_rel.with_suffix(''), section_dir)
    return rel.replace('\\', '/')


def render_toctree(label: str, entries: list, section_dir: Path) -> str:
    """
    entries 是 walk_section 返回的列表。把同级 leaves 合并到一个 toctree 块。
    嵌套子组：用子组 label 作为 caption 单独再起一个 toctree。
    简化策略：把所有 leaf（不管多深）按 caption=label 全部摊平进一个 toctree。
    这样侧边栏 maxdepth 控制层级，不会丢内容。
    """
    leaves = []
    def collect(es):
        for lbl, val in es:
            if isinstance(val, Path):
                leaves.append(val)
            else:
                collect(val)
    collect(entries)
    if not leaves:
        return ''
    lines = ['```{toctree}', ':maxdepth: 2', f':caption: {label}', '']
    for tgt in leaves:
        lines.append(relpath_for_toctree(tgt, section_dir))
    lines.append('```')
    return '\n'.join(lines)


def render_section_index(section_label: str, section_dir_name: str,
                          tree: list) -> str:
    """生成某个 section 的 index.md。tree 是 walk_section 返回的根列表。"""
    section_dir = Path(section_dir_name)
    body = [f'# {section_label}', '']

    # 顶级 leaves 自成一组（可能是欢迎页之类的零散文件）
    top_leaves = [(lbl, val) for lbl, val in tree if isinstance(val, Path)]
    sub_groups = [(lbl, val) for lbl, val in tree if isinstance(val, list)]

    if top_leaves:
        block = render_toctree('概述', top_leaves, section_dir)
        if block:
            body.append(block)
            body.append('')

    for lbl, sub in sub_groups:
        block = render_toctree(lbl, sub, section_dir)
        if block:
            body.append(block)
            body.append('')

    return '\n'.join(body).rstrip() + '\n'


def main():
    nav = yaml.safe_load(MKDOCS_YML.read_text(encoding='utf-8')).get('nav', [])
    # nav 形如 [{'MatrixOne': [...]}]
    assert nav and 'MatrixOne' in nav[0]
    top_items = nav[0]['MatrixOne']

    # 拷图片
    imgs_src = SRC_DOCS / 'MatrixOne' / 'images'
    if imgs_src.exists():
        imgs_dst = DST_ROOT / 'images'
        if imgs_dst.exists():
            shutil.rmtree(imgs_dst)
        shutil.copytree(imgs_src, imgs_dst)
        print(f"images: {imgs_src} → {imgs_dst}")

    total_copied: list[tuple[str, Path]] = []

    for item in top_items:
        assert isinstance(item, dict) and len(item) == 1
        label, value = next(iter(item.items()))

        if isinstance(value, str):
            # 顶级 leaf：主页 / 名词术语表
            # demo 有自己策划的 index.md，不要被 mkdocs README 覆盖
            if value == 'README.md':
                print(f"[skip ] {label} ({value}) — demo 主页已策划")
                continue
            rel = copy_one(value)
            if rel is not None:
                total_copied.append((value, rel))
                print(f"[leaf] {label} → {rel}")
            continue

        # 顶级分组
        section_dir_name = SECTION_DIR.get(label)
        if not section_dir_name:
            print(f"  ! unmapped section: {label}", file=sys.stderr)
            continue
        print(f"\n[section] {label} → {section_dir_name}/")
        tree = walk_section(value, total_copied)
        index_text = render_section_index(label, section_dir_name, tree)
        index_path = DST_ROOT / section_dir_name / 'index.md'
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text(index_text, encoding='utf-8')
        print(f"   index.md → {index_path.relative_to(DST_ROOT)}")

    print(f"\nTotal markdown files copied: {len(total_copied)}")


if __name__ == '__main__':
    main()
