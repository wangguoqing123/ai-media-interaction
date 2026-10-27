#!/usr/bin/env python3
"""Read the bundled, offline casebook. No credentials or network required."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from urllib.parse import urlparse

SKILL_ROOT = Path(__file__).resolve().parents[1]
CASEBOOK = SKILL_ROOT / "references" / "cases.json"


def load_casebook():
    return json.loads(CASEBOOK.read_text(encoding="utf-8"))


def title(case):
    return case["title"] or "封面：" + case["cover_text"] + "（无独立标题）"


def markdown_case(case):
    image = SKILL_ROOT / case["cover_file"]
    body = case["body"] if case["body_status"] == "present" else "原帖未显示单独文字正文，仅参考封面。"
    notes = "\n".join("- " + note for note in case["adaptation_notes"])
    return (
        f"## {case['id']}｜{case['author']}\n\n"
        f"- 原始标题：{case['title'] or '未设置独立标题'}\n"
        f"- 封面文字：{case['cover_text']}\n"
        f"- 原帖：{case['source_url']}\n"
        f"- 记录日期：{case['snapshot_date']}\n"
        f"- 类型：{case['interaction_family']}\n"
        f"- 核心问题：{case['core_question']}\n"
        f"- 期待回应：{case['response_action']}\n"
        f"- 本地封面：{image}\n\n"
        f"### 正文学习摘要\n\n{body}\n\n"
        f"### 结构观察\n\n{case['structure']}\n\n"
        f"### 可迁移与不可照搬\n\n{notes}\n"
    )


def check(book):
    cases = book["cases"]
    errors = []
    if book.get("case_count") != len(cases):
        errors.append("case_count与实际记录数不一致")
    for field in ("id", "note_id"):
        values = [c.get(field) for c in cases]
        if len(set(values)) != len(values) or not all(values):
            errors.append(f"{field}缺失或重复")
    for case in cases:
        prefix = case.get("id", "unknown")
        for field in ("author", "cover_text", "source_url", "snapshot_date", "interaction_family", "core_question", "response_action", "structure", "cover_file", "cover_sha256"):
            if not case.get(field):
                errors.append(f"{prefix}: 缺少{field}")
        path = Path(case.get("cover_file", ""))
        image = (SKILL_ROOT / path).resolve()
        if path.is_absolute() or not image.is_relative_to(SKILL_ROOT):
            errors.append(f"{prefix}: 图片路径必须位于Skill内")
        elif not image.is_file():
            errors.append(f"{prefix}: 图片不存在")
        elif hashlib.sha256(image.read_bytes()).hexdigest() != case.get("cover_sha256"):
            errors.append(f"{prefix}: 图片校验不一致")
        url = urlparse(case.get("source_url", ""))
        if url.scheme != "https" or url.hostname != "www.xiaohongshu.com" or url.query or url.fragment:
            errors.append(f"{prefix}: 需使用不带临时参数的原帖链接")
        status = case.get("body_status")
        if status not in ("present", "not_shown"):
            errors.append(f"{prefix}: 正文状态不明确")
        if (status == "present") != bool(case.get("body")):
            errors.append(f"{prefix}: 原文与正文状态不一致")
        if case.get("title") is None and not case.get("cover_text"):
            errors.append(f"{prefix}: 无标题时需保留真实封面文字")
    return {"ok": not errors, "case_count": len(cases), "cover_count": sum((SKILL_ROOT / c.get("cover_file", "")).is_file() for c in cases), "errors": errors}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    listing = commands.add_parser("list", help="查看索引，可按可迁移方向或互动类型筛选")
    listing.add_argument("--direction")
    listing.add_argument("--family")
    listing.add_argument("--format", choices=("markdown", "json"), default="markdown")
    showing = commands.add_parser("show", help="完整读取指定案例及本地封面路径")
    showing.add_argument("ids", nargs="+")
    showing.add_argument("--format", choices=("markdown", "json"), default="markdown")
    commands.add_parser("check", help="检查数据、来源、缺失状态和封面完整性")
    args = parser.parse_args()
    book = load_casebook()
    cases = book["cases"]
    if args.command == "check":
        report = check(book)
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if report["ok"] else 1
    if args.command == "show":
        by_id = {c["id"]: c for c in cases}
        missing = [i for i in args.ids if i not in by_id]
        if missing:
            parser.error("未知案例编号：" + "、".join(missing))
        selected = [by_id[i] for i in dict.fromkeys(args.ids)]
        if args.format == "json":
            print(json.dumps(selected, ensure_ascii=False, indent=2))
        else:
            print("\n".join(markdown_case(c) for c in selected))
        return 0
    selected = cases
    if args.direction:
        query = args.direction.casefold()
        selected = [c for c in selected if any(query in d.casefold() for d in c["transfer_directions"])]
    if args.family:
        selected = [c for c in selected if args.family.casefold() in c["interaction_family"].casefold()]
    if args.format == "json":
        print(json.dumps([{k: c[k] for k in ("id", "author", "title", "cover_text", "interaction_family", "core_question", "response_action", "transfer_directions", "cover_file")} for c in selected], ensure_ascii=False, indent=2))
    else:
        print("| 编号 | 作者／标题 | 互动目的 | 核心问题 | 可迁移方向 |")
        print("|---|---|---|---|---|")
        for case in selected:
            print(f"| {case['id']} | {case['author']}：{title(case)} | {case['interaction_family']} | {case['core_question']} | {'、'.join(case['transfer_directions'])} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
