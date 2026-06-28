#!/usr/bin/env python3
"""Render Markdown into WeChat-friendly inline-styled HTML.

This script is intentionally local. It does not call md2wechat.cn, upload images,
or create WeChat drafts.
"""

from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

THEMES = {
    "clean-tech": {
        "page_bg": "#f6f8fb",
        "paper_bg": "#ffffff",
        "text": "#263241",
        "muted": "#667085",
        "accent": "#2563eb",
        "accent_2": "#10b981",
        "accent_soft": "#eff6ff",
        "surface": "#f8fbff",
        "surface_2": "#f0f7ff",
        "border": "#d9e2ef",
        "code_bg": "#f2f5f9",
        "shadow": "0 18px 45px rgba(37, 99, 235, 0.08)",
        "radius": "14px",
        "label": "开场笔记",
    },
    "warm-editorial": {
        "page_bg": "#fbf7f0",
        "paper_bg": "#fffdf8",
        "text": "#3f352f",
        "muted": "#7a6a60",
        "accent": "#b35c2e",
        "accent_2": "#d68b45",
        "accent_soft": "#fff1e7",
        "surface": "#fff8ef",
        "surface_2": "#f8eadb",
        "border": "#ead8c7",
        "code_bg": "#f7eee6",
        "shadow": "0 18px 44px rgba(179, 92, 46, 0.10)",
        "radius": "16px",
        "label": "开场笔记",
    },
    "minimal-ink": {
        "page_bg": "#f7f7f5",
        "paper_bg": "#ffffff",
        "text": "#202124",
        "muted": "#62666d",
        "accent": "#111827",
        "accent_2": "#6b7280",
        "accent_soft": "#f1f2f4",
        "surface": "#fafafa",
        "surface_2": "#eeeeee",
        "border": "#dedede",
        "code_bg": "#f4f4f4",
        "shadow": "0 16px 42px rgba(17, 24, 39, 0.07)",
        "radius": "10px",
        "label": "短札",
    },
    "wechat-green": {
        "page_bg": "#f5fbf7",
        "paper_bg": "#ffffff",
        "text": "#24342e",
        "muted": "#68756f",
        "accent": "#07c160",
        "accent_2": "#10a37f",
        "accent_soft": "#eefbf4",
        "surface": "#f7fffa",
        "surface_2": "#eaf8f0",
        "border": "#d8eadf",
        "code_bg": "#f2f8f5",
        "shadow": "0 18px 45px rgba(7, 193, 96, 0.08)",
        "radius": "14px",
        "label": "微信笔记",
    },
    "press-card": {
        "page_bg": "#f5f2eb",
        "paper_bg": "#fffdf7",
        "text": "#24211c",
        "muted": "#746f66",
        "accent": "#9a3412",
        "accent_2": "#1f2937",
        "accent_soft": "#f8ead7",
        "surface": "#fff8ea",
        "surface_2": "#efe3cf",
        "border": "#e0d4bf",
        "code_bg": "#f3eadb",
        "shadow": "0 18px 46px rgba(36, 33, 28, 0.09)",
        "radius": "8px",
        "label": "简报",
    },
    "tufte-ink": {
        "page_bg": "#fbfaf6",
        "paper_bg": "#fffffb",
        "text": "#222222",
        "muted": "#6f6a60",
        "accent": "#8a4b2a",
        "accent_2": "#475569",
        "accent_soft": "#f4efe7",
        "surface": "#fbf7ef",
        "surface_2": "#efe8dc",
        "border": "#ddd3c2",
        "code_bg": "#f5f1ea",
        "shadow": "0 12px 36px rgba(34, 34, 34, 0.06)",
        "radius": "6px",
        "label": "旁注",
    },
    "magazine-editorial": {
        "page_bg": "#f3f0ea",
        "paper_bg": "#fffefa",
        "text": "#1f2933",
        "muted": "#6f746d",
        "accent": "#0f4c5c",
        "accent_2": "#c1663b",
        "accent_soft": "#eaf3f4",
        "surface": "#f7f2e8",
        "surface_2": "#e7eee9",
        "border": "#d8d1c3",
        "code_bg": "#eef2f0",
        "shadow": "0 18px 48px rgba(15, 76, 92, 0.08)",
        "radius": "12px",
        "label": "编辑导读",
    },
    "newspaper-press": {
        "page_bg": "#f4f1eb",
        "paper_bg": "#fffdfa",
        "text": "#191919",
        "muted": "#66615a",
        "accent": "#8b1e16",
        "accent_2": "#1f2937",
        "accent_soft": "#f5e8e4",
        "surface": "#faf4e9",
        "surface_2": "#ede2d0",
        "border": "#d9cdbb",
        "code_bg": "#efe8dc",
        "shadow": "0 12px 34px rgba(25, 25, 25, 0.06)",
        "radius": "4px",
        "label": "新闻简报",
    },
    "swiss-product": {
        "page_bg": "#f4f7fb",
        "paper_bg": "#ffffff",
        "text": "#111827",
        "muted": "#5b6472",
        "accent": "#0057ff",
        "accent_2": "#ff5a1f",
        "accent_soft": "#eaf1ff",
        "surface": "#f8fbff",
        "surface_2": "#edf4ff",
        "border": "#d6e1f2",
        "code_bg": "#f0f4fa",
        "shadow": "0 18px 48px rgba(0, 87, 255, 0.09)",
        "radius": "6px",
        "label": "产品笔记",
    },
    "ink-literary": {
        "page_bg": "#f8f7f2",
        "paper_bg": "#fffef8",
        "text": "#25221d",
        "muted": "#716a5d",
        "accent": "#5c4033",
        "accent_2": "#8b7355",
        "accent_soft": "#f1ebe0",
        "surface": "#faf6ee",
        "surface_2": "#eee5d8",
        "border": "#ddd2c1",
        "code_bg": "#f3eee5",
        "shadow": "0 12px 34px rgba(92, 64, 51, 0.06)",
        "radius": "3px",
        "label": "墨色札记",
    },
    "bold-opinion": {
        "page_bg": "#f7f7f2",
        "paper_bg": "#fffdf6",
        "text": "#111111",
        "muted": "#5f5b54",
        "accent": "#d62828",
        "accent_2": "#003049",
        "accent_soft": "#ffe8e6",
        "surface": "#fff4e6",
        "surface_2": "#f3dfc1",
        "border": "#e4cfb3",
        "code_bg": "#f7ead7",
        "shadow": "0 16px 42px rgba(214, 40, 40, 0.08)",
        "radius": "8px",
        "label": "观点",
    },
}

SCENE_THEME_MAP = {
    "tutorial": "clean-tech",
    "教程": "clean-tech",
    "指南": "clean-tech",
    "technical": "clean-tech",
    "tech": "clean-tech",
    "how-to": "clean-tech",
    "guide": "clean-tech",
    "product": "swiss-product",
    "产品": "swiss-product",
    "发布": "swiss-product",
    "launch": "swiss-product",
    "analysis": "magazine-editorial",
    "分析": "magazine-editorial",
    "深度分析": "magazine-editorial",
    "report": "magazine-editorial",
    "strategy": "magazine-editorial",
    "news": "newspaper-press",
    "新闻": "newspaper-press",
    "热点": "newspaper-press",
    "briefing": "newspaper-press",
    "essay": "warm-editorial",
    "随笔": "warm-editorial",
    "个人随笔": "warm-editorial",
    "personal": "warm-editorial",
    "interview": "magazine-editorial",
    "访谈": "magazine-editorial",
    "对话": "magazine-editorial",
    "dialogue": "magazine-editorial",
    "case-study": "press-card",
    "案例": "press-card",
    "复盘": "press-card",
    "review": "press-card",
    "listicle": "wechat-green",
    "清单": "wechat-green",
    "checklist": "wechat-green",
    "literary": "ink-literary",
    "文学": "ink-literary",
    "文化": "ink-literary",
    "culture": "ink-literary",
    "opinion": "bold-opinion",
    "观点": "bold-opinion",
    "评论": "bold-opinion",
    "commentary": "bold-opinion",
}

VISUAL_DIRECTION_THEME = {
    "clear-engineering": "clean-tech",
    "engineering": "clean-tech",
    "工程感": "clean-tech",
    "清爽技术": "clean-tech",
    "modern-product-editorial": "swiss-product",
    "product-editorial": "swiss-product",
    "swiss-product": "swiss-product",
    "产品感": "swiss-product",
    "瑞士风": "swiss-product",
    "magazine-editorial": "magazine-editorial",
    "magazine": "magazine-editorial",
    "杂志感": "magazine-editorial",
    "杂志风": "magazine-editorial",
    "press-newsroom": "newspaper-press",
    "newsroom": "newspaper-press",
    "newspaper": "newspaper-press",
    "报纸感": "newspaper-press",
    "新闻感": "newspaper-press",
    "warm-human-editorial": "warm-editorial",
    "warm-human": "warm-editorial",
    "温暖叙事": "warm-editorial",
    "quiet-ink": "ink-literary",
    "ink": "ink-literary",
    "水墨": "ink-literary",
    "文学感": "ink-literary",
    "bold-opinion": "bold-opinion",
    "opinion": "bold-opinion",
    "观点感": "bold-opinion",
    "wechat-native": "wechat-green",
    "微信原生": "wechat-green",
}


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---", 4)
    if end == -1:
        return {}, text
    raw = text[4:end].strip()
    body = text[text.find("\n", end + 1) + 1 :]
    meta: dict[str, str] = {}
    for line in raw.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip().strip('"').strip("'")
        meta[key.strip().lower()] = value
    return meta, body.lstrip()


def normalize_key(value: str) -> str:
    value = strip_inline_markdown(value).strip().lower()
    value = re.sub(r"[\s_/]+", "-", value)
    value = re.sub(r"[^a-z0-9\u4e00-\u9fff-]+", "", value)
    return value.strip("-")


def infer_article_type(meta: dict[str, str], markdown: str) -> str:
    explicit = first_meta(meta, "article_type", "type", "scene", "scenario", "category")
    if explicit:
        key = normalize_key(explicit)
        if key in SCENE_THEME_MAP:
            return key

    sample = strip_inline_markdown(markdown).lower()
    compact = sample.replace(" ", "")
    rules = [
        ("interview", ["访谈", "对话", "q&a", "问答", "我：", "你："]),
        ("tutorial", ["教程", "指南", "上手", "步骤", "安装", "配置", "命令", "api", "cli", "```"]),
        ("product", ["产品", "发布", "功能", "版本", "上线", "工具", "体验", "能力"]),
        ("case-study", ["复盘", "案例", "事故", "项目", "实践", "经验"]),
        ("news", ["新闻", "热点", "最新", "今天", "刚刚", "速览", "快讯"]),
        ("opinion", ["观点", "评论", "我认为", "为什么说", "争议"]),
        ("literary", ["读书", "文学", "文化", "艺术", "诗", "散文"]),
        ("essay", ["随笔", "个人", "想法", "感受", "生活", "故事"]),
        ("listicle", ["清单", "合集", "推荐", "盘点", "收藏"]),
        ("analysis", ["分析", "趋势", "报告", "研究", "战略", "行业"]),
    ]
    for scene, needles in rules:
        if any(needle.lower() in sample or needle.lower() in compact for needle in needles):
            return scene
    return "analysis"


def first_meta(meta: dict[str, str], *keys: str) -> str:
    for key in keys:
        value = meta.get(key)
        if value:
            return value
    return ""


def resolve_theme(theme_name: str, meta: dict[str, str], markdown: str) -> tuple[str, str]:
    if theme_name != "auto":
        return theme_name, infer_article_type(meta, markdown)

    visual = first_meta(meta, "visual_direction", "visual", "aesthetic", "style")
    if visual:
        visual_key = normalize_key(visual)
        if visual_key in THEMES:
            return visual_key, infer_article_type(meta, markdown)
        if visual_key in VISUAL_DIRECTION_THEME:
            return VISUAL_DIRECTION_THEME[visual_key], infer_article_type(meta, markdown)

    scene = infer_article_type(meta, markdown)
    return SCENE_THEME_MAP.get(scene, "magazine-editorial"), scene


def extract_title(meta: dict[str, str], markdown: str) -> str:
    if meta.get("title"):
        return meta["title"]
    for line in markdown.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line)
        if match:
            return strip_inline_markdown(match.group(1))
    return "Wechat Article"


def strip_inline_markdown(value: str) -> str:
    value = re.sub(r"`([^`]+)`", r"\1", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    value = re.sub(r"\*([^*]+)\*", r"\1", value)
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    return value.strip()


def inline(text: str, theme: dict[str, str]) -> str:
    placeholders: list[str] = []

    def stash(value: str) -> str:
        placeholders.append(value)
        return f"\u0000{len(placeholders) - 1}\u0000"

    escaped = html.escape(text, quote=False)

    escaped = re.sub(
        r"!\[([^\]]*)\]\(([^)]+)\)",
        lambda m: stash(
            f'<img src="{html.escape(m.group(2), quote=True)}" alt="{html.escape(m.group(1), quote=True)}" '
            f'style="display:block;width:100%;max-width:100%;height:auto;margin:18px auto;border-radius:8px;" />'
        ),
        escaped,
    )
    escaped = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda m: stash(
            f'<a href="{html.escape(m.group(2), quote=True)}" '
            f'style="color:{theme["accent"]};text-decoration:none;border-bottom:1px solid {theme["accent"]};">'
            f"{m.group(1)}</a>"
        ),
        escaped,
    )
    escaped = re.sub(
        r"`([^`]+)`",
        lambda m: stash(
            f'<code style="background:{theme["code_bg"]};color:{theme["accent"]};'
            f'padding:2px 5px;border-radius:4px;font-size:0.92em;">{m.group(1)}</code>'
        ),
        escaped,
    )
    escaped = re.sub(
        r"\*\*([^*]+)\*\*",
        rf'<strong style="color:{theme["accent"]};font-weight:700;">\1</strong>',
        escaped,
    )
    escaped = re.sub(
        r"==([^=]+)==",
        rf'<mark style="background:{theme["accent_soft"]};color:{theme["accent"]};padding:1px 4px;border-radius:4px;">\1</mark>',
        escaped,
    )
    escaped = re.sub(
        r"~~([^~]+)~~",
        rf'<span style="color:{theme["muted"]};text-decoration:line-through;">\1</span>',
        escaped,
    )
    escaped = re.sub(r"\*([^*]+)\*", r'<em style="font-style:italic;">\1</em>', escaped)

    for index, value in enumerate(placeholders):
        escaped = escaped.replace(f"\u0000{index}\u0000", value)
    return escaped


def is_table_start(lines: list[str], i: int) -> bool:
    if i + 1 >= len(lines):
        return False
    return "|" in lines[i] and re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", lines[i + 1]) is not None


def split_table_row(line: str) -> list[str]:
    line = line.strip().strip("|")
    return [cell.strip() for cell in line.split("|")]


def render_table(lines: list[str], start: int, theme: dict[str, str]) -> tuple[str, int]:
    header = split_table_row(lines[start])
    rows: list[list[str]] = []
    i = start + 2
    while i < len(lines) and "|" in lines[i].strip():
        rows.append(split_table_row(lines[i]))
        i += 1

    parts = [
        f'<table style="width:100%;border-collapse:collapse;margin:18px 0;color:{theme["text"]};font-size:14px;">',
        "<thead><tr>",
    ]
    for cell in header:
        parts.append(
            f'<th style="border:1px solid {theme["border"]};background:{theme["accent_soft"]};'
            f'padding:9px;text-align:left;color:{theme["accent"]};font-weight:700;">{inline(cell, theme)}</th>'
        )
    parts.append("</tr></thead><tbody>")
    for row in rows:
        parts.append("<tr>")
        for cell in row:
            parts.append(
                f'<td style="border:1px solid {theme["border"]};padding:9px;vertical-align:top;">{inline(cell, theme)}</td>'
            )
        parts.append("</tr>")
    parts.append("</tbody></table>")
    return "".join(parts), i


def paragraph(text: str, theme: dict[str, str], lead: bool = False) -> str:
    if lead:
        return (
            f'<section style="margin:0 0 24px;padding:18px 18px 16px;background:{theme["surface"]};'
            f'border:1px solid {theme["border"]};border-radius:{theme["radius"]};box-shadow:{theme["shadow"]};">'
            f'<div style="margin:0 0 8px;color:{theme["accent"]};font-size:11px;line-height:1;'
            f'font-weight:800;letter-spacing:0.08em;text-transform:uppercase;">{theme["label"]}</div>'
            f'<p style="margin:0;color:{theme["text"]};font-size:17px;line-height:1.88;'
            f'font-weight:500;">{inline(text, theme)}</p></section>'
        )
    return (
        f'<p style="margin:0 0 17px;color:{theme["text"]};font-size:16px;'
        f'line-height:1.9;">{inline(text, theme)}</p>'
    )


def render_callout(kind: str, title: str, body_lines: list[str], theme: dict[str, str]) -> str:
    kind_key = normalize_key(kind or "note")
    labels = {
        "important": "重点",
        "tip": "提示",
        "warning": "避雷",
        "note": "笔记",
        "callout": "笔记",
    }
    label = labels.get(kind_key, kind_key)
    body = " ".join(line.strip() for line in body_lines if line.strip())
    title_html = (
        f'<div style="margin:0 0 8px;color:{theme["text"]};font-size:17px;line-height:1.5;font-weight:800;">'
        f'{inline(title, theme)}</div>'
        if title
        else ""
    )
    body_html = (
        f'<p style="margin:0;color:{theme["text"]};font-size:15px;line-height:1.82;">{inline(body, theme)}</p>'
        if body
        else ""
    )
    return (
        f'<section style="margin:22px 0;padding:16px 17px;background:{theme["accent_soft"]};'
        f'border:1px solid {theme["border"]};border-left:5px solid {theme["accent"]};'
        f'border-radius:{theme["radius"]};box-shadow:{theme["shadow"]};">'
        f'<div style="margin:0 0 8px;color:{theme["accent"]};font-size:11px;font-weight:850;'
        f'letter-spacing:0.08em;">{label}</div>{title_html}{body_html}</section>'
    )


def render_container(kind: str, title: str, content_lines: list[str], theme: dict[str, str]) -> str:
    kind_key = normalize_key(kind)
    title = title.strip()
    lines = [line.strip() for line in content_lines if line.strip()]
    if kind_key == "stat":
        metric = lines[0] if lines else title
        detail = " ".join(lines[1:]) if len(lines) > 1 else ""
        label = title or "关键数字"
        detail_html = (
            f'<p style="margin:8px 0 0;color:{theme["muted"]};font-size:14px;line-height:1.72;">'
            f'{inline(detail, theme)}</p>'
            if detail
            else ""
        )
        return (
            f'<section style="margin:24px 0;padding:18px 18px;background:{theme["surface"]};'
            f'border:1px solid {theme["border"]};border-radius:{theme["radius"]};box-shadow:{theme["shadow"]};">'
            f'<div style="margin:0 0 8px;color:{theme["accent"]};font-size:11px;font-weight:850;'
            f'letter-spacing:0.08em;">{inline(label, theme)}</div>'
            f'<div style="color:{theme["text"]};font-size:30px;line-height:1.18;font-weight:900;">'
            f'{inline(metric, theme)}</div>{detail_html}</section>'
        )

    if kind_key == "dialogue":
        parts = []
        if title:
            parts.append(
                f'<div style="margin:0 0 12px;color:{theme["accent"]};font-size:12px;font-weight:850;'
                f'letter-spacing:0.08em;">{inline(title, theme)}</div>'
            )
        for line in lines:
            speaker, sep, words = line.partition(":")
            if not sep:
                speaker, sep, words = line.partition("：")
            if sep and words.strip():
                parts.append(
                    f'<div style="margin:0 0 12px;padding:12px 13px;background:{theme["paper_bg"]};'
                    f'border:1px solid {theme["border"]};border-radius:10px;">'
                    f'<span style="display:block;margin:0 0 4px;color:{theme["accent"]};font-size:12px;font-weight:800;">'
                    f'{inline(speaker.strip(), theme)}</span>'
                    f'<span style="display:block;color:{theme["text"]};font-size:15px;line-height:1.78;">'
                    f'{inline(words.strip(), theme)}</span></div>'
                )
            else:
                parts.append(paragraph(line, theme))
        return (
            f'<section style="margin:24px 0;padding:16px;background:{theme["surface"]};'
            f'border:1px solid {theme["border"]};border-radius:{theme["radius"]};">'
            f'{"".join(parts)}</section>'
        )

    if kind_key == "gallery":
        items = []
        for line in lines:
            match = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", line)
            if match:
                items.append(
                    f'<figure style="margin:0 0 14px;">'
                    f'<img src="{html.escape(match.group(2), quote=True)}" alt="{html.escape(match.group(1), quote=True)}" '
                    f'style="display:block;width:100%;height:auto;border-radius:{theme["radius"]};" />'
                    f'<figcaption style="margin:7px 0 0;color:{theme["muted"]};font-size:12px;line-height:1.6;">'
                    f'{html.escape(match.group(1))}</figcaption></figure>'
                )
        label = (
            f'<div style="margin:0 0 12px;color:{theme["accent"]};font-size:12px;font-weight:850;'
            f'letter-spacing:0.08em;">{inline(title, theme)}</div>'
            if title
            else ""
        )
        return (
            f'<section style="margin:24px 0;padding:15px;background:{theme["surface"]};'
            f'border:1px solid {theme["border"]};border-radius:{theme["radius"]};">'
            f'{label}{"".join(items)}</section>'
        )

    if kind_key == "byline":
        body = " ".join(lines)
        label = title or "作者手记"
        return (
            f'<section style="margin:28px 0 4px;padding:17px 18px;background:{theme["surface"]};'
            f'border:1px solid {theme["border"]};border-radius:{theme["radius"]};">'
            f'<div style="margin:0 0 8px;color:{theme["accent"]};font-size:12px;font-weight:850;">'
            f'{inline(label, theme)}</div>'
            f'<p style="margin:0;color:{theme["text"]};font-size:15px;line-height:1.82;">{inline(body, theme)}</p>'
            f'</section>'
        )

    return render_callout(kind_key or "note", title, lines, theme)


def normalized_plain(value: str) -> str:
    return re.sub(r"\s+", "", strip_inline_markdown(value)).strip().lower()


def render_markdown(
    markdown: str,
    theme_name: str,
    document_title: str = "",
    meta: dict[str, str] | None = None,
) -> str:
    resolved_theme, _ = resolve_theme(theme_name, meta or {}, markdown)
    theme = THEMES[resolved_theme]
    lines = markdown.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    blocks: list[str] = []
    para: list[str] = []
    in_code = False
    code_lang = ""
    code_lines: list[str] = []
    i = 0
    first_body_h1_seen = False
    lead_done = False

    def flush_para() -> None:
        nonlocal lead_done
        if para:
            text = " ".join(x.strip() for x in para).strip()
            blocks.append(paragraph(text, theme, lead=not lead_done))
            lead_done = True
            para.clear()

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            if not in_code:
                flush_para()
                in_code = True
                code_lang = stripped[3:].strip()
                code_lines = []
            else:
                escaped = html.escape("\n".join(code_lines))
                label = (
                    f'<div style="color:{theme["accent"]};font-size:12px;margin-bottom:8px;font-weight:700;">{html.escape(code_lang)}</div>'
                    if code_lang
                    else ""
                )
                blocks.append(
                    f'<section style="margin:20px 0;padding:16px 17px;background:{theme["code_bg"]};'
                    f'border:1px solid {theme["border"]};border-radius:{theme["radius"]};overflow:auto;">'
                    f'{label}<pre style="margin:0;color:{theme["text"]};font-size:13px;line-height:1.65;'
                    f'white-space:pre-wrap;"><code>{escaped}</code></pre></section>'
                )
                in_code = False
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        if not stripped:
            flush_para()
            i += 1
            continue

        if is_table_start(lines, i):
            flush_para()
            table_html, i = render_table(lines, i, theme)
            blocks.append(table_html)
            continue

        container = re.match(r"^:::\s*([A-Za-z0-9_-]+)(?:\[(.*?)\])?\s*$", stripped)
        if container:
            flush_para()
            kind = container.group(1)
            title = container.group(2) or ""
            i += 1
            content_lines = []
            while i < len(lines) and lines[i].strip() != ":::":
                content_lines.append(lines[i])
                i += 1
            if i < len(lines) and lines[i].strip() == ":::":
                i += 1
            blocks.append(render_container(kind, title, content_lines, theme))
            continue

        if stripped == "---":
            flush_para()
            blocks.append(
                f'<section style="margin:30px 0;text-align:center;">'
                f'<span style="display:inline-block;width:56px;border-top:2px solid {theme["accent"]};opacity:0.55;"></span>'
                f'</section>'
            )
            i += 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            flush_para()
            level = len(heading.group(1))
            raw_heading = heading.group(2).strip()
            if (
                level == 1
                and not first_body_h1_seen
                and document_title
                and normalized_plain(raw_heading) == normalized_plain(document_title)
            ):
                first_body_h1_seen = True
                i += 1
                continue
            if level == 1:
                first_body_h1_seen = True
            text = inline(raw_heading, theme)
            if level == 1:
                blocks.append(
                    f'<h1 style="margin:2px 0 24px;color:{theme["text"]};font-size:25px;line-height:1.35;'
                    f'font-weight:850;">{text}</h1>'
                )
            elif level == 2:
                blocks.append(
                    f'<h2 style="margin:34px 0 16px;padding:0 0 0 12px;'
                    f'border-left:4px solid {theme["accent"]};color:{theme["text"]};font-size:21px;'
                    f'line-height:1.45;font-weight:800;">{text}</h2>'
                )
            else:
                blocks.append(
                    f'<h3 style="margin:23px 0 12px;color:{theme["accent"]};font-size:17px;line-height:1.5;'
                    f'font-weight:760;">{text}</h3>'
                )
            i += 1
            continue

        if stripped.startswith(">"):
            flush_para()
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            callout_match = re.match(r"^\[!([A-Za-z0-9_-]+)\]\s*(.*)$", quote_lines[0] if quote_lines else "")
            if callout_match:
                blocks.append(
                    render_callout(
                        callout_match.group(1),
                        callout_match.group(2).strip(),
                        quote_lines[1:],
                        theme,
                    )
                )
                continue
            quote_body = "<br />".join(inline(x, theme) for x in quote_lines if x)
            blocks.append(
                f'<blockquote style="position:relative;margin:22px 0;padding:18px 18px 18px 20px;'
                f'background:{theme["accent_soft"]};border:1px solid {theme["border"]};'
                f'border-left:5px solid {theme["accent"]};border-radius:{theme["radius"]};'
                f'color:{theme["text"]};line-height:1.84;box-shadow:{theme["shadow"]};">'
                f'<span style="display:block;color:{theme["accent"]};font-size:30px;line-height:0.8;'
                f'font-weight:900;opacity:0.35;">&ldquo;</span>'
                f'<span>{quote_body}</span></blockquote>'
            )
            continue

        if re.match(r"^([-*+])\s+", stripped) or re.match(r"^\d+\.\s+", stripped):
            flush_para()
            ordered = re.match(r"^\d+\.\s+", stripped) is not None
            items = []
            pattern = r"^\d+\.\s+" if ordered else r"^[-*+]\s+"
            n = 1
            while i < len(lines) and re.match(pattern, lines[i].strip()):
                item = re.sub(pattern, "", lines[i].strip())
                marker = str(n) if ordered else ""
                marker_html = (
                    f'<span style="display:inline-block;min-width:22px;height:22px;margin-right:9px;'
                    f'border-radius:999px;background:{theme["accent"]};color:#ffffff;text-align:center;'
                    f'line-height:22px;font-size:12px;font-weight:800;">{marker}</span>'
                    if ordered
                    else f'<span style="display:inline-block;width:8px;height:8px;margin:9px 12px 0 2px;'
                    f'border-radius:999px;background:{theme["accent"]};vertical-align:top;"></span>'
                )
                items.append(
                    f'<div style="display:flex;align-items:flex-start;margin:0 0 10px;padding:11px 12px;'
                    f'background:{theme["surface"]};border:1px solid {theme["border"]};'
                    f'border-radius:10px;color:{theme["text"]};line-height:1.78;">'
                    f'{marker_html}<span style="flex:1;">{inline(item, theme)}</span></div>'
                )
                n += 1
                i += 1
            blocks.append(f'<section style="margin:0 0 20px;">{"".join(items)}</section>')
            continue

        para.append(line)
        i += 1

    flush_para()
    return "\n".join(blocks)


def compact_wechat_html(article_html: str) -> str:
    """Remove tag-boundary whitespace that WeChat may turn into empty paragraphs."""
    compacted = re.sub(r">\s+<", "><", article_html.strip())
    return re.sub(r"<p[^>]*>\s*</p>", "", compacted).strip()


def build_full_page(article_html: str, title: str, meta: dict[str, str], theme_name: str) -> str:
    theme = THEMES[theme_name]
    author = meta.get("author", "")
    digest = meta.get("digest") or meta.get("summary") or meta.get("description") or ""
    author_line = (
        f'<span style="display:inline-block;margin:0 8px 8px 0;color:{theme["muted"]};font-size:13px;'
        f'line-height:1.6;">By {html.escape(author)}</span>'
        if author
        else ""
    )
    digest_line = (
        f'<p style="margin:16px 0 0;color:{theme["muted"]};font-size:15px;line-height:1.75;">{html.escape(digest)}</p>'
        if digest
        else ""
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
</head>
<body style="margin:0;background:{theme["page_bg"]};">
  <main style="box-sizing:border-box;max-width:760px;margin:0 auto;padding:30px 13px 52px;">
    <article style="box-sizing:border-box;background:{theme["paper_bg"]};border:1px solid {theme["border"]};
      border-radius:{theme["radius"]};padding:28px 22px;color:{theme["text"]};font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Arial,'PingFang SC','Microsoft YaHei',sans-serif;box-shadow:{theme["shadow"]};">
      <header style="margin-bottom:24px;padding-bottom:20px;border-bottom:1px solid {theme["border"]};">
        <div style="margin:0 0 12px;color:{theme["accent"]};font-size:11px;font-weight:850;letter-spacing:0.10em;">WECHAT DRAFT</div>
        <h1 style="margin:0 0 12px;color:{theme["text"]};font-size:29px;line-height:1.32;font-weight:900;">{html.escape(title)}</h1>
        <div>{author_line}<span style="display:inline-block;color:{theme["muted"]};font-size:13px;">{theme_name}</span></div>
        {digest_line}
      </header>
      {article_html}
    </article>
  </main>
</body>
</html>
"""


def choose_output(input_path: Path, fragment: bool) -> Path:
    suffix = ".fragment.html" if fragment else ".wechat.html"
    return input_path.with_suffix(suffix)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render Markdown to local WeChat-friendly HTML.")
    parser.add_argument("markdown", type=Path, help="Input Markdown file")
    parser.add_argument("-o", "--output", type=Path, help="Output HTML file")
    parser.add_argument("--theme", choices=sorted([*THEMES, "auto"]), default="auto")
    parser.add_argument("--fragment", action="store_true", help="Write only the article body HTML")
    parser.add_argument("--compact", action="store_true", help="Compact fragment HTML for WeChat submission")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    text = args.markdown.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(text)
    title = extract_title(meta, body)
    resolved_theme, article_type = resolve_theme(args.theme, meta, body)
    article_html = render_markdown(body, resolved_theme, document_title=title, meta=meta)
    output = args.output or choose_output(args.markdown, args.fragment)
    output.parent.mkdir(parents=True, exist_ok=True)
    if args.compact:
        article_html = compact_wechat_html(article_html)
    final = article_html if args.fragment else build_full_page(article_html, title, meta, resolved_theme)
    output.write_text(final, encoding="utf-8")
    print(f"Wrote {output} (theme={resolved_theme}, article_type={article_type})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
