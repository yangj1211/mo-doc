#!/usr/bin/env python3
"""批量翻译 zh markdown → en,用 Claude API。

用法
----
先 export ANTHROPIC_API_KEY=...,然后:

  uv run python scripts/translate_batch.py --product matrixone-intelligence --dry-run
      # 看一下要翻多少篇,估个 token 预算

  uv run python scripts/translate_batch.py --product matrixone-intelligence --limit 5
      # 只翻 5 篇,人肉 review 翻译质量

  uv run python scripts/translate_batch.py --product matrixone-intelligence
      # 全量,默认跳过已存在的 en 文件;断了重跑能续

  uv run python scripts/translate_batch.py --product matrixone-intelligence --force
      # 强制重翻所有

设计要点
--------
1. **保留原 markdown 结构**:代码块、MyST 指令、`[](url)` 链接、`<doc/path>` toctree
   引用、frontmatter、HTML 标签等全部不动,只翻人类可读文本。提示词里硬约束。
2. **glossary 一致性**:scripts/translate_glossary.md 注入到 system prompt,
   保证 "工作区"、"数据探索" 这种产品名词全站统一。
3. **断点续翻**:跳过已存在的 en 文件。失败的不会写出 en 文件,所以下次重跑会自动重试。
4. **并发**:asyncio + semaphore,默认 8 路。Anthropic API rate limit 一般够用。
5. **大文件**:单文件 max_tokens 16K 够覆盖 99% 文档;实在装不下的会被报告出来,
   人工切分或单独提高 max_tokens。
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
import time
from pathlib import Path

import anthropic


REPO = Path(__file__).resolve().parent.parent
GLOSSARY_PATH = Path(__file__).resolve().parent / "translate_glossary.md"


SYSTEM_PROMPT = """You are a professional technical translator working on MatrixOne and MatrixOne Intelligence developer documentation. Your job is to translate Chinese markdown source files into natural, professional English suitable for a developer audience.

CRITICAL RULES — these are non-negotiable; violating any one breaks the build:

1. PRESERVE ALL MARKDOWN STRUCTURE EXACTLY.
   - Headings (`#`, `##`, ...), bullet/numbered lists, tables, blockquotes, frontmatter (`--- yaml ---`), bold/italic markers, horizontal rules.
   - Indentation and blank lines around block-level elements.

2. PRESERVE ALL FENCED CODE BLOCKS UNCHANGED.
   - Anything between ` ``` ` (or `~~~`) — including the language tag, code, SQL keywords, command output, file paths, comments inside code, log lines — stays byte-for-byte identical.
   - Inline code `like this` also stays identical.

3. PRESERVE ALL MyST DIRECTIVES.
   - Block directives like ` ```{note} `, ` ```{tip} `, ` ```{warning} `, ` ```{toctree} `, ` ```{tab-set} `, ` ```{tab-item} `, ` ```{grid} `, ` ```{grid-item-card} ` — keep the directive name and option lines (lines starting with `:`) UNCHANGED. Translate ONLY the human-readable body.
   - Inside ` ```{toctree} ` blocks, entries look like `Title <doc/path>` — translate the Title, keep `<doc/path>` exactly.

4. LINKS AND IMAGES.
   - For `[text](url)` and `[text](url "title")`: translate `text`, keep `url` exactly. Translate `title` if present.
   - For `![alt](url)`: translate `alt`, keep `url` exactly.
   - For HTML `<a href="...">text</a>`, `<img alt="..." src="...">`: translate visible text / alt, keep attributes.

5. ATTRIBUTE BLOCKS like `{.mo-hero-title}`, `{.mo-subtitle}`, `:link: foo/bar`, `:link-type: doc`, `:class-card: mo-entry-card` — keep UNCHANGED.

6. HTML TAGS pass through (`<br>`, `<details>`, `<summary>`, etc.). Translate text between tags.

7. TERMINOLOGY CONSISTENCY.
   - Use the glossary below for product-specific terms. Render exactly as the right-hand column.
   - For terms not in the glossary, prefer the most common English usage in cloud / database documentation.

8. WRITING STYLE.
   - Active voice, present tense, second person ("you") for instructions.
   - Concise sentences; one idea per sentence.
   - Don't translate Chinese idioms literally — adapt to natural English.

9. OUTPUT FORMAT.
   - Output ONLY the translated markdown content.
   - NO preamble ("Here is the translation..."), NO commentary, NO trailing notes.
   - DO NOT wrap your output in a ` ```markdown ` fence. The markdown source itself may contain fences; you write it raw.

GLOSSARY
--------
{glossary}
"""


def load_glossary() -> str:
    return GLOSSARY_PATH.read_text(encoding="utf-8")


def collect_pairs(zh_root: Path, en_root: Path, force: bool) -> list[tuple[Path, Path]]:
    pairs = []
    for src in sorted(zh_root.rglob("*.md")):
        rel = src.relative_to(zh_root)
        dst = en_root / rel
        if dst.exists() and not force:
            continue
        pairs.append((src, dst))
    return pairs


def estimate_tokens(text: str) -> int:
    """粗算:1 token ≈ 1.5 个中文字符 / 4 个英文字符。文档以中文为主,按 ~2 char/token 估。"""
    return max(1, len(text) // 2)


async def translate_one(
    client: anthropic.AsyncAnthropic,
    src: Path,
    dst: Path,
    model: str,
    max_tokens: int,
    system: str,
) -> tuple[str, int, int]:
    content = src.read_text(encoding="utf-8")
    if not content.strip():
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(content, encoding="utf-8")
        return ("empty", 0, 0)

    msg = await client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": content}],
    )
    out = msg.content[0].text

    # 兜底:模型偶尔会自作主张包一层 ```markdown 围栏,剥掉
    stripped = out.strip()
    if stripped.startswith("```markdown\n") and stripped.endswith("\n```"):
        out = stripped[len("```markdown\n") : -len("\n```")] + "\n"
    elif stripped.startswith("```\n") and stripped.endswith("\n```"):
        # 极少见情况:无语言 tag。只在首尾对称时剥
        if stripped.count("```") == 2:
            out = stripped[len("```\n") : -len("\n```")] + "\n"

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(out, encoding="utf-8")
    in_t = msg.usage.input_tokens
    out_t = msg.usage.output_tokens
    return ("ok", in_t, out_t)


async def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--product", choices=["matrixone", "matrixone-intelligence"], required=True)
    parser.add_argument("--limit", type=int, default=0, help="只翻前 N 个 (0=全部)")
    parser.add_argument("--dry-run", action="store_true", help="只列表 + 估算,不真翻")
    parser.add_argument("--force", action="store_true", help="即使 en 已存在也重翻")
    parser.add_argument("--model", default="claude-haiku-4-5-20251001",
                        help="default haiku 4.5(便宜快);大文件可用 claude-sonnet-4-6")
    parser.add_argument("--max-tokens", type=int, default=16384)
    parser.add_argument("--concurrency", type=int, default=8)
    args = parser.parse_args()

    src_root = REPO / args.product / "source" / "zh"
    dst_root = REPO / args.product / "source" / "en"

    if not src_root.exists():
        print(f"找不到 {src_root}", file=sys.stderr)
        sys.exit(1)

    pairs = collect_pairs(src_root, dst_root, args.force)
    if args.limit > 0:
        pairs = pairs[: args.limit]

    print(f"== {args.product}")
    print(f"  zh:{src_root}")
    print(f"  en:{dst_root}")
    print(f"  待翻 {len(pairs)} 个文件 (model={args.model}, concurrency={args.concurrency})")

    if not pairs:
        print("没有要翻的(en 已全量存在,或加 --force)")
        return

    # 估算 token
    total_chars = sum(p[0].stat().st_size for p in pairs)
    est_in = total_chars // 2
    est_out = int(est_in * 1.3)
    print(f"  源文件总字节 ~{total_chars/1024:.1f} KB")
    print(f"  估算 input ~{est_in:,} tokens, output ~{est_out:,} tokens")

    if args.dry_run:
        for src, dst in pairs[:30]:
            print(f"    {src.relative_to(src_root)}")
        if len(pairs) > 30:
            print(f"    ... ({len(pairs)-30} more)")
        return

    if "ANTHROPIC_API_KEY" not in os.environ:
        print("\n请先 export ANTHROPIC_API_KEY=...", file=sys.stderr)
        sys.exit(1)

    glossary = load_glossary()
    system = SYSTEM_PROMPT.format(glossary=glossary)

    client = anthropic.AsyncAnthropic()
    sem = asyncio.Semaphore(args.concurrency)
    started_at = time.time()
    done = 0
    err = 0
    in_total = 0
    out_total = 0
    lock = asyncio.Lock()

    async def worker(src: Path, dst: Path):
        nonlocal done, err, in_total, out_total
        async with sem:
            try:
                status, in_t, out_t = await translate_one(
                    client, src, dst, args.model, args.max_tokens, system
                )
            except Exception as e:
                async with lock:
                    err += 1
                    done += 1
                print(f"[{done}/{len(pairs)}] ✗ {src.relative_to(src_root)}: {type(e).__name__}: {e}")
                return
            async with lock:
                done += 1
                in_total += in_t
                out_total += out_t
                cur = done
            tag = "✓" if status == "ok" else "-"
            print(f"[{cur}/{len(pairs)}] {tag} {src.relative_to(src_root)} ({in_t}+{out_t} tokens)")

    await asyncio.gather(*(worker(s, d) for s, d in pairs))

    elapsed = time.time() - started_at
    print(f"\n完成。{done - err} 成功 / {err} 失败,耗时 {elapsed:.1f}s")
    print(f"实际 token:input {in_total:,} + output {out_total:,} = {in_total + out_total:,}")


if __name__ == "__main__":
    asyncio.run(main())
