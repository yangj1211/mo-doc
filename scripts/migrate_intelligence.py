#!/usr/bin/env python3
"""
将 moc-docs (mkdocs) 全量内容迁移到 docs-demo/intelligence/。

前置：
  - 已经 cp -R moc-docs/docs/MatrixOne-Intelligence/ → docs-demo/intelligence/
  - 已经 mv "intelligence/workflow api" → "intelligence/workflow-api"

本脚本完成的事：
  1. 把 intelligence/**/*.md 里的 MkDocs 专属语法转 MyST
       - !!! note "Title" + 缩进块  →  :::{note} Title ... :::
       - === "Tab"     + 缩进块  →  ::::{tab-set} :::{tab-item} Tab ::: ::::
       - workflow api/ / workflow%20api/  →  workflow-api/
  2. 解析 moc-docs/mkdocs.yml 的 nav，按顶层分组生成 section index.md
  3. 生成 intelligence/index.md（hero + 入口卡片 + 隐藏 toctree）

设计取舍：
  - 文件保留 moc-docs 原始大小写（App-Develop / Workspace-Mgmt 等不动），
    避免大量内部链接断裂；只处理 workflow api 这一处空格目录名。
  - 顶层 nav 分组的 section index 用扁平命名（intro / start / genai-workspace
    / db-instance / monitoring / alerts / event-list / billing / releases / protocols），
    避开和已有大小写相近的 disk dir 冲突。
"""
import re
import sys
from pathlib import Path
import yaml

ROOT = Path('/Users/admin/project/moi/docs-demo/intelligence')
MKDOCS_YML = Path('/Users/admin/project/moi/doc/moc-docs/mkdocs.yml')


# -------------------------------------------------------------------
# 1. 语法转换
# -------------------------------------------------------------------

# 匹配一行 admonition 起始：!!! note  或  !!! warning "标题"
ADMONITION_TYPES = {
    'note', 'tip', 'info', 'warning', 'danger', 'caution',
    'attention', 'hint', 'important', 'error', 'example',
    'success', 'question', 'quote', 'abstract', 'summary',
    'todo', 'bug', 'failure', 'seealso',
}
# MyST 支持的 admonition 类型范围比 MkDocs 更窄，做一次 fallback 映射
ADMONITION_REMAP = {
    'abstract': 'note',
    'summary': 'note',
    'info': 'note',
    'todo': 'note',
    'success': 'tip',
    'question': 'note',
    'quote': 'note',
    'failure': 'error',
    'bug': 'error',
    'example': 'note',
    'attention': 'warning',
    'caution': 'warning',
}

ADMONITION_RE = re.compile(
    r'^(?P<indent>[ \t]*)!!!\s+(?P<type>[a-z]+)\s*(?:"(?P<title>[^"]*)")?\s*$'
)
TAB_HEADER_RE = re.compile(
    r'^(?P<indent>[ \t]*)===\s+"(?P<title>[^"]+)"\s*$'
)


def _is_indented_into(line: str, base_indent: str) -> bool:
    """该行是否属于 base_indent 之后的'更深一级缩进'块（4 空格 / 1 tab）。"""
    if not line.strip():
        return True  # 空行不打断块
    body = line.rstrip('\n')
    # 至少要在 base_indent 之上多出一级缩进
    if body.startswith(base_indent + '    '):
        return True
    if body.startswith(base_indent + '\t'):
        return True
    return False


def _dedent_block(lines: list[str], base_indent: str) -> list[str]:
    """把 admonition / tab 内部的缩进块去掉一级缩进。"""
    out = []
    deeper4 = base_indent + '    '
    deeper_tab = base_indent + '\t'
    for ln in lines:
        if not ln.strip():
            out.append('')
            continue
        if ln.startswith(deeper4):
            out.append(ln[len(deeper4):].rstrip('\n'))
        elif ln.startswith(deeper_tab):
            out.append(ln[len(deeper_tab):].rstrip('\n'))
        else:
            out.append(ln.rstrip('\n'))
    # 去掉首尾连续空行
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return out


def convert_admonitions_and_tabs(text: str) -> tuple[str, int, int]:
    """单个文件的转换。返回 (新文本, admonition 命中数, tab-set 命中数)。"""
    lines = text.split('\n')
    out: list[str] = []
    i = 0
    n = len(lines)
    n_adm = 0
    n_tabset = 0

    while i < n:
        line = lines[i]
        m_adm = ADMONITION_RE.match(line)
        m_tab = TAB_HEADER_RE.match(line)

        if m_adm:
            indent = m_adm.group('indent')
            atype = m_adm.group('type').lower()
            atitle = m_adm.group('title') or ''
            # MyST 不识别的 type 做映射
            myst_type = ADMONITION_REMAP.get(atype, atype)
            if myst_type not in ADMONITION_TYPES - set(ADMONITION_REMAP):
                # 兜底：未知类型一律退成 note
                myst_type = 'note'

            # 收集后续缩进块
            body: list[str] = []
            j = i + 1
            # 至少跳过紧随其后的空行
            while j < n and not lines[j].strip():
                body.append('')
                j += 1
            while j < n and _is_indented_into(lines[j], indent):
                body.append(lines[j])
                j += 1
                # 一段连续缩进块结束于第一个不再缩进的非空行

            dedented = _dedent_block(body, indent)
            # 输出 :::{note} Title  ...  :::（保留原 indent，让嵌套场景下还在父 list 里）
            head = f'{indent}:::{{{myst_type}}}'
            if atitle:
                head += f' {atitle}'
            out.append(head)
            for b in dedented:
                out.append(f'{indent}{b}' if b else '')
            out.append(f'{indent}:::')
            n_adm += 1
            i = j
            continue

        if m_tab:
            # 收集连续的 === "Title" 块
            indent = m_tab.group('indent')
            tab_blocks: list[tuple[str, list[str]]] = []
            j = i
            while j < n:
                mt = TAB_HEADER_RE.match(lines[j])
                if not mt or mt.group('indent') != indent:
                    break
                title = mt.group('title')
                body: list[str] = []
                k = j + 1
                while k < n and not lines[k].strip():
                    body.append('')
                    k += 1
                while k < n and _is_indented_into(lines[k], indent):
                    body.append(lines[k])
                    k += 1
                tab_blocks.append((title, _dedent_block(body, indent)))
                j = k
                # 跳过 tab 之间的空行
                while j < n and not lines[j].strip():
                    j += 1

            # 渲染为 sphinx-design tab-set。
            # colon_fence 嵌套规则：外层 fence 必须比内层多 1 个冒号。
            # tab-item 内常嵌入 :::{note}（3 冒号），所以 tab-item 用 4，tab-set 用 5。
            out.append(f'{indent}:::::{{tab-set}}')
            for title, body in tab_blocks:
                out.append('')
                out.append(f'{indent}::::{{tab-item}} {title}')
                for b in body:
                    out.append(f'{indent}{b}' if b else '')
                out.append(f'{indent}::::')
            out.append(f'{indent}:::::')
            n_tabset += 1
            i = j
            continue

        out.append(line)
        i += 1

    return '\n'.join(out), n_adm, n_tabset


WORKFLOW_API_RE = re.compile(r'workflow(?: |%20)api/')


def fix_workflow_api_links(text: str) -> tuple[str, int]:
    new_text, n = WORKFLOW_API_RE.subn('workflow-api/', text)
    return new_text, n


def step1_convert_all():
    files = sorted(ROOT.rglob('*.md'))
    total_adm = 0
    total_tab = 0
    total_link = 0
    files_changed = 0
    for f in files:
        original = f.read_text(encoding='utf-8')
        new1, n_adm, n_tab = convert_admonitions_and_tabs(original)
        new2, n_link = fix_workflow_api_links(new1)
        if new2 != original:
            f.write_text(new2, encoding='utf-8')
            files_changed += 1
        total_adm += n_adm
        total_tab += n_tab
        total_link += n_link
    print(f'[step1] files scanned:    {len(files)}')
    print(f'[step1] files changed:    {files_changed}')
    print(f'[step1] admonitions:      {total_adm}')
    print(f'[step1] tab-set blocks:   {total_tab}')
    print(f'[step1] workflow-api fix: {total_link}')


# -------------------------------------------------------------------
# 2. nav → section index.md
# -------------------------------------------------------------------

# MkDocs nav path 里的目录是 'workflow api'，映射到磁盘的 'workflow-api'
def normalize_nav_path(p: str) -> str:
    return p.replace('workflow api/', 'workflow-api/')


def md_path_to_docref(md_path: str) -> str:
    """
    'MatrixOne-Intelligence/Get-Started/quickstart.md'
      → 'Get-Started/quickstart'
    moc-docs 的 mkdocs.yml 有 4 处把 'MatrixOne-Intelligence/Reference/...' 误写成
    'MatrixOne/Reference/...'（SHOW PITR / SHOW SNAPSHOTS / DECODE / ENCODE）。
    在这里统一吃掉，使 toctree 能落到磁盘上真实存在的路径。
    """
    p = normalize_nav_path(md_path)
    if p.startswith('MatrixOne-Intelligence/'):
        p = p[len('MatrixOne-Intelligence/'):]
    elif p.startswith('MatrixOne/'):
        # moc-docs nav 内的笔误，纠回 intelligence 自己的目录
        p = p[len('MatrixOne/'):]
    if p.endswith('.md'):
        p = p[:-3]
    return p


def doc_exists(docref: str) -> bool:
    return (ROOT / f'{docref}.md').is_file()


def collect_leaves(items, out: list[tuple[str, str]], missing: list[str]):
    """递归把所有 leaf (label, md path) 摊平。
    moc-docs 的 nav 里有几条指向已删文件的死链（CREATE/ALTER/DROP ACCOUNT 等），
    这里按磁盘真实存在过滤掉，并记到 missing 里方便审。
    """
    for item in items:
        if not isinstance(item, dict) or len(item) != 1:
            continue
        label, value = next(iter(item.items()))
        if isinstance(value, str):
            if value.startswith('http'):
                continue
            docref = md_path_to_docref(value)
            if not doc_exists(docref):
                missing.append(value)
                continue
            out.append((label, value))
        elif isinstance(value, list):
            collect_leaves(value, out, missing)


def render_section_index(title: str, groups: list[tuple[str, list[tuple[str, str]]]]) -> str:
    """
    groups: [(caption, [(label, md_path), ...]), ...]
    每个 caption 一个 toctree 块。已在 collect_leaves 阶段过滤过 missing。
    section 内按 docref 去重（保留首次出现），覆盖两类源头重复：
      1. moc-docs 自己的 nav 里 LPAD 出现两次
      2. SHOW PITR / SHOW SNAPSHOTS / DECODE / ENCODE 既出现在 nav（错前缀
         被纠回），又被当作孤儿登记，会重复
    """
    seen: set[str] = set()
    body = [f'# {title}', '']
    for caption, leaves in groups:
        deduped: list[tuple[str, str]] = []
        for label, md_path in leaves:
            docref = md_path_to_docref(md_path)
            if docref in seen:
                continue
            seen.add(docref)
            deduped.append((label, md_path))
        if not deduped:
            continue
        body.append('```{toctree}')
        body.append(':maxdepth: 2')
        body.append(f':caption: {caption}')
        body.append('')
        for _label, md_path in deduped:
            body.append(md_path_to_docref(md_path))
        body.append('```')
        body.append('')
    return '\n'.join(body).rstrip() + '\n'


# 孤儿文件（mkdocs nav 没收录的）→ 手动归到对应 section
ORPHAN_ASSIGNMENT: dict[str, tuple[str, str]] = {
    # docref（无 .md）→ (section_index_name, 标签)
    'Get-Started/ai_search':                                '快速开始 (start)',
    'Get-Started/cv_search':                                '快速开始 (start)',
    'Get-Started/parse_demo':                               '快速开始 (start)',
    'Overview/mone-introduction':                           '关于 (intro)',
    'Reference/SQL-Reference/Data-Definition-Language/restore-account':
        '数据库实例 (db-instance)',
    'Reference/SQL-Reference/Other/Partition/mo-partition-support':
        '数据库实例 (db-instance)',
    'Reference/Operators/operators/cast-functions-and-operators/decode':
        '数据库实例 (db-instance)',
    'Reference/Operators/operators/cast-functions-and-operators/encode':
        '数据库实例 (db-instance)',
    'Reference/SQL-Reference/Other/SHOW-Statements/show-pitr':
        '数据库实例 (db-instance)',
    'Reference/SQL-Reference/Other/SHOW-Statements/show-snapshots':
        '数据库实例 (db-instance)',
}

ORPHAN_TO_SECTION = {
    'Get-Started/ai_search':                                'start',
    'Get-Started/cv_search':                                'start',
    'Get-Started/parse_demo':                               'start',
    'Overview/mone-introduction':                           'intro',
    'Reference/SQL-Reference/Data-Definition-Language/restore-account': 'db-instance',
    'Reference/SQL-Reference/Other/Partition/mo-partition-support':     'db-instance',
    'Reference/Operators/operators/cast-functions-and-operators/decode': 'db-instance',
    'Reference/Operators/operators/cast-functions-and-operators/encode': 'db-instance',
    'Reference/SQL-Reference/Other/SHOW-Statements/show-pitr':           'db-instance',
    'Reference/SQL-Reference/Other/SHOW-Statements/show-snapshots':      'db-instance',
}


# 顶层 nav 分组 → (section index 文件名 (无 .md), 入口卡 emoji, 入口卡描述)
SECTION_META = {
    '关于 MatrixOne Intelligence':
        ('intro',           '📐', '了解 MatrixOne Intelligence 的产品定位、核心能力与 MySQL 兼容性。'),
    '快速开始':
        ('start',           '🚀', '从创建 GenAI 工作区到第一条向量查询，5 分钟完成上手闭环。'),
    'GenAI 工作区':
        ('genai-workspace', '🧠', 'GenAI 工作区的工作流、连接器、数据探索、用户权限和 API 全景。'),
    '数据库实例':
        ('db-instance',     '🗄️', '实例创建、连接、迁移、备份、安全与完整 SQL 参考。'),
    '监控':
        ('monitoring',      '📊', '监控指标和监控数据视图。'),
    '告警':
        ('alerts',          '🔔', '告警规则与事件订阅。'),
    '事件':
        ('event-list',      '📜', '系统事件清单。'),
    '计费':
        ('billing',         '💳', '充值、卡券、账单、价格、变更与退订全流程。'),
    '版本发布纪要':
        ('releases',        '📦', '历年版本发布说明。'),
    '相关协议':
        ('protocols',       '📋', '隐私协议、服务条款、SLA。'),
}


def step2_generate_indices():
    nav = yaml.safe_load(MKDOCS_YML.read_text(encoding='utf-8')).get('nav', [])
    # 顶层是 [{'MatrixOne Intelligence': [...]}, {'MatrixOne': 'https://...'}]
    moi_block = None
    for entry in nav:
        if isinstance(entry, dict) and 'MatrixOne Intelligence' in entry:
            moi_block = entry['MatrixOne Intelligence']
            break
    assert moi_block, 'mkdocs.yml 找不到 MatrixOne Intelligence 顶层 nav'

    section_files: list[tuple[str, str]] = []  # (title, docref)
    leaf_root_files: list[tuple[str, str]] = []  # (title, docref)
    section_groups: dict[str, list[tuple[str, list[tuple[str, str]]]]] = {}
    all_missing: list[str] = []

    for entry in moi_block:
        if not isinstance(entry, dict) or len(entry) != 1:
            continue
        label, value = next(iter(entry.items()))

        if isinstance(value, str):
            # 顶层 leaf：主页 / 技术支持 / 术语表
            if value == 'README.md':
                continue  # demo 自己写主页
            docref = md_path_to_docref(value)
            leaf_root_files.append((label, docref))
            print(f'[leaf]   {label} → {docref}')
            continue

        if not isinstance(value, list):
            continue

        meta = SECTION_META.get(label)
        if not meta:
            print(f'  ! 未配置 section meta: {label}', file=sys.stderr)
            continue
        section_name = meta[0]

        # 把这个 section 的子项分成 (caption, leaves) 列表
        # 规则：直接 leaf → 进 "概述" 组；子 dict → 用其 label 作为 caption，
        # 内部 leaves（递归全部摊平）作为 toctree 内容
        groups: list[tuple[str, list[tuple[str, str]]]] = []
        overview: list[tuple[str, str]] = []
        for sub in value:
            if not isinstance(sub, dict) or len(sub) != 1:
                continue
            sub_label, sub_val = next(iter(sub.items()))
            if isinstance(sub_val, str):
                if sub_val.startswith('http'):
                    continue
                overview.append((sub_label, sub_val))
            elif isinstance(sub_val, list):
                leaves: list[tuple[str, str]] = []
                collect_leaves(sub_val, leaves, all_missing)
                if leaves:
                    groups.append((sub_label, leaves))
        if overview:
            # overview 自身也可能有死链
            overview_clean: list[tuple[str, str]] = []
            for lbl, mp in overview:
                if doc_exists(md_path_to_docref(mp)):
                    overview_clean.append((lbl, mp))
                else:
                    all_missing.append(mp)
            if overview_clean:
                groups.insert(0, ('概述', overview_clean))

        section_groups[section_name] = groups
        section_files.append((label, section_name))

    # 把孤儿文件归并到 section_groups 里（统一一个 "其他" caption 块）
    orphans_by_section: dict[str, list[tuple[str, str]]] = {}
    for docref, sec in ORPHAN_TO_SECTION.items():
        if not doc_exists(docref):
            continue
        # 用文件名（去 / 去 - 还原）作为标签，最终页面会用文件 H1
        fname = docref.rsplit('/', 1)[-1]
        # md_path 形式：'MatrixOne-Intelligence/...' 让 md_path_to_docref 还原
        md_path = f'MatrixOne-Intelligence/{docref}.md'
        orphans_by_section.setdefault(sec, []).append((fname, md_path))

    for sec, items in orphans_by_section.items():
        section_groups.setdefault(sec, []).append(('其他', items))

    # 真正写盘
    for sec_name, groups in section_groups.items():
        # 找出 section 的中文 label（用来当 H1）
        section_label = next(
            (lbl for lbl, n in section_files if n == sec_name), sec_name
        )
        index_text = render_section_index(section_label, groups)
        (ROOT / f'{sec_name}.md').write_text(index_text, encoding='utf-8')
        n_leaves = sum(len(g[1]) for g in groups)
        print(f'[index]  {section_label} → {sec_name}.md  ({len(groups)} groups, {n_leaves} leaves)')

    if all_missing:
        print(f'\n[skip ] {len(all_missing)} 条 nav 死链已跳过：')
        for m in all_missing:
            print(f'         {m}')

    # ---------------------------------------------------------------
    # 3. root index.md（matrixone 首页同款简洁版）
    #    - 大标题：产品 slogan（不带"文档"二字）
    #    - 副标题：一行
    #    - 4 张入口卡片（图标由 _static/js/icons.js 注入，无 emoji）
    #    - 隐藏 master toctree（侧边栏导航全集）
    # ---------------------------------------------------------------
    HOME_CARDS = [
        # title, docref, description (15-25 字)
        ('5 分钟上手',  'Get-Started/quickstart',
         '从创建工作区到第一条向量查询的最小路径'),
        ('核心概念',    'Overview/matrixone-intelligence-introduction',
         '理解平台定位、能力边界与多模态数据架构'),
        ('API 参考',    'workflow-api/automic_api',
         '工作流原子能力与数据接入 / 处理 / 探索的接口规范'),
        ('常见问题',    'FAQs/FAQ-Product',
         '实例、计费、连接、限制等高频疑问解答'),
    ]
    cards: list[str] = []
    for title, docref, desc in HOME_CARDS:
        if not doc_exists(docref):
            print(f'  ! 首页卡片目标不存在: {docref}', file=sys.stderr)
            continue
        cards.append(
            f':::{{grid-item-card}} {title}\n'
            f':link: {docref}\n'
            f':link-type: doc\n'
            f':class-card: mo-entry-card\n\n'
            f'{desc}\n'
            f':::\n'
        )

    master_toc_lines = ['主页 <self>']
    for title, docref in section_files:
        master_toc_lines.append(f'{title} <{docref}>')
    for title, docref in leaf_root_files:
        master_toc_lines.append(f'{title} <{docref}>')

    root_md = (
        '{.mo-hero-title}\n'
        '# 一站式 DATA + AI 平台\n\n'
        '{.mo-subtitle}\n'
        '覆盖数据治理、文档智能、Agent 构建，从数据到 AI 应用全链路\n\n'
        '::::{grid} 1 2 2 2\n'
        ':gutter: 3\n'
        ':margin: 4 0 4 0\n\n'
        + '\n'.join(cards) +
        '\n::::\n\n'
        '```{toctree}\n'
        ':caption: MatrixOne Intelligence\n'
        ':maxdepth: 1\n'
        ':hidden:\n\n'
        + '\n'.join(master_toc_lines) + '\n'
        '```\n'
    )
    (ROOT / 'index.md').write_text(root_md, encoding='utf-8')
    print(f'\n[root]  index.md  ({len(cards)} cards, '
          f'{len(section_files)} sections + {len(leaf_root_files)} leaves in toctree)')


def main():
    print('=== STEP 1: convert syntax ===')
    step1_convert_all()
    print('\n=== STEP 2: generate section indices + root ===')
    step2_generate_indices()
    print('\nDone.')


if __name__ == '__main__':
    main()
