#!/usr/bin/env python3
"""把 MkDocs 风格的 admonition / tab 在所有 .md 里就地转成 MyST。

MkDocs 写法 → MyST:
    !!! note                       →  :::{note}
    !!! note "Title"               →  :::{note} Title
    !!! Note 注意                  →  :::{note} 注意       (大小写不敏感)
    !!! info 注意                  →  :::{note} 注意       (info 映射到 note)
    !!! 注意                       →  :::{note}            (中文 type → 映射)
    === "Tab"                      →  ::::{tab-item} Tab   (外层 tab-set 自动包)

跟 migrate_intelligence.py 里的转换器同源,这里把:
  1. type 正则放宽到 [^\s]+ 接受任意非空白
  2. 大小写折叠
  3. 中文 type 词表映射

用法:
    uv run python scripts/convert_admonitions.py [<dir> ...]

默认目标:
    matrixone/source/zh
    matrixone/source/en
    matrixone-intelligence/source/zh
    matrixone-intelligence/source/en
"""
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DEFAULT_TARGETS = [
    REPO / 'matrixone' / 'source' / 'zh',
    REPO / 'matrixone' / 'source' / 'en',
    REPO / 'matrixone-intelligence' / 'source' / 'zh',
    REPO / 'matrixone-intelligence' / 'source' / 'en',
]

MYST_NATIVE = {
    'note', 'tip', 'warning', 'danger', 'important', 'hint',
    'attention', 'caution', 'error', 'seealso',
}
ADMONITION_REMAP = {
    'abstract': 'note', 'summary': 'note', 'info': 'note',
    'todo': 'note', 'success': 'tip', 'question': 'note',
    'quote': 'note', 'failure': 'error', 'bug': 'error',
    'example': 'note',
}
CHINESE_TYPE_MAP = {
    '注意': 'note', '提示': 'tip', '警告': 'warning',
    '重要': 'important', '例子': 'note', '信息': 'note',
    '危险': 'danger',
}

ADMONITION_RE = re.compile(r'^(?P<indent>[ \t]*)!!!\s+(?P<rest>.+?)\s*$')
TAB_HEADER_RE = re.compile(r'^(?P<indent>[ \t]*)===\s+"(?P<title>[^"]+)"\s*$')


def parse_head(rest: str) -> tuple[str, str]:
    """解析 `!!! ` 之后的部分,返回 (myst_type, title)。"""
    m = re.match(r'^(\S+)\s+"([^"]*)"\s*$', rest)
    if m:
        first, title = m.group(1), m.group(2)
    else:
        parts = rest.split(None, 1)
        first = parts[0]
        title = parts[1] if len(parts) > 1 else ''

    if first in CHINESE_TYPE_MAP:
        return CHINESE_TYPE_MAP[first], title.strip()
    flc = first.lower()
    if flc in MYST_NATIVE:
        return flc, title.strip()
    if flc in ADMONITION_REMAP:
        return ADMONITION_REMAP[flc], title.strip()
    # 完全不识别 → 整个 rest 当标题,type 兜底成 note
    return 'note', rest.strip()


def is_indented(line: str, base: str) -> bool:
    """该行是否属于"比 base 缩进更深一级"。tab 和空格混用统一展成 4-space 等宽再判。"""
    if not line.strip():
        return True
    expanded = line.expandtabs(4).rstrip('\n')
    expanded_base = base.expandtabs(4)
    if not expanded.startswith(expanded_base):
        return False
    rest = expanded[len(expanded_base):]
    return bool(rest) and rest[0] == ' '


def dedent(lines: list[str], base: str) -> list[str]:
    """剥掉一级缩进。统一用 expandtabs(4) 处理 tab/空格混用,输出全部用空格。"""
    out = []
    expanded_base = base.expandtabs(4)
    for ln in lines:
        if not ln.strip():
            out.append('')
            continue
        expanded = ln.expandtabs(4).rstrip('\n')
        if expanded.startswith(expanded_base + '    '):
            out.append(expanded[len(expanded_base) + 4:])
        elif expanded.startswith(expanded_base):
            # 至少剥掉 base,剩余前导空格保留(可能是不规则缩进)
            out.append(expanded[len(expanded_base):].lstrip(' '))
        else:
            out.append(expanded)
    while out and not out[0].strip():
        out.pop(0)
    while out and not out[-1].strip():
        out.pop()
    return out


def convert(text: str) -> tuple[str, int, int]:
    lines = text.split('\n')
    out, i, n_adm, n_tabset = [], 0, 0, 0
    n = len(lines)

    while i < n:
        line = lines[i]
        m_adm = ADMONITION_RE.match(line)
        m_tab = TAB_HEADER_RE.match(line)

        if m_adm:
            indent = m_adm.group('indent')
            myst_type, title = parse_head(m_adm.group('rest'))

            body, j = [], i + 1
            while j < n and not lines[j].strip():
                body.append('')
                j += 1
            while j < n and is_indented(lines[j], indent):
                body.append(lines[j])
                j += 1

            head = f'{indent}:::{{{myst_type}}}'
            if title:
                head += f' {title}'
            out.append(head)
            for b in dedent(body, indent):
                out.append(f'{indent}{b}' if b else '')
            out.append(f'{indent}:::')
            n_adm += 1
            i = j
            continue

        if m_tab:
            indent = m_tab.group('indent')
            blocks = []
            j = i
            while j < n:
                mt = TAB_HEADER_RE.match(lines[j])
                if not mt or mt.group('indent') != indent:
                    break
                title = mt.group('title')
                body, k = [], j + 1
                while k < n and not lines[k].strip():
                    body.append('')
                    k += 1
                while k < n and is_indented(lines[k], indent):
                    body.append(lines[k])
                    k += 1
                blocks.append((title, dedent(body, indent)))
                j = k
                while j < n and not lines[j].strip():
                    j += 1

            # tab-item 内常嵌 :::{note}(3 冒号),所以 tab-item 用 4,tab-set 用 5
            out.append(f'{indent}:::::{{tab-set}}')
            for title, body in blocks:
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


def main(argv: list[str]) -> int:
    targets = [Path(p) for p in argv] if argv else DEFAULT_TARGETS
    total_files = total_adm = total_tab = 0
    for root in targets:
        if not root.exists():
            print(f"skip (missing): {root}", file=sys.stderr)
            continue
        for md in sorted(root.rglob('*.md')):
            text = md.read_text(encoding='utf-8')
            new_text, n_adm, n_tab = convert(text)
            if n_adm == 0 and n_tab == 0:
                continue
            md.write_text(new_text, encoding='utf-8')
            total_files += 1
            total_adm += n_adm
            total_tab += n_tab
            rel = md.relative_to(REPO)
            print(f"  {rel}  ({n_adm} adm, {n_tab} tab)")
    print(f"\nDone. {total_files} files, {total_adm} admonitions, {total_tab} tab-sets.")
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
