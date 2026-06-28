#!/usr/bin/env python3
"""Create a practical image plan for a WeChat article."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import render_wechat_html


MODE_LABELS = {
    "cover": "Editorial Cover / Key Visual",
    "workflow": "Step / Workflow Graphic",
    "chat": "Chat / AI Conversation Mockup",
    "route": "Route / Map / Travel Guide Graphic",
    "bento": "Bento / High-Density Information Graphic",
    "lifestyle": "Product / Lifestyle Scene",
}


def plain_text(markdown: str) -> str:
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", markdown)
    text = render_wechat_html.strip_inline_markdown(text)
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return text


def keywords(text: str) -> set[str]:
    compact = text.lower().replace(" ", "")
    return {compact}


def detect_modes(markdown: str, requested: list[str]) -> list[str]:
    if requested:
        return ["cover", *[mode for mode in requested if mode != "cover"]]

    text = plain_text(markdown)
    compact = text.lower().replace(" ", "")
    modes = ["cover"]

    if any(x in compact for x in ["步骤", "流程", "教程", "四个阶段", "step", "workflow", "发布流程"]):
        modes.append("workflow")
    if any(x in compact for x in ["聊天", "对话", "prompt", "提示词", "ai", "一句话", "客服"]):
        modes.append("chat")
    if any(x in compact for x in ["旅行", "路线", "地图", "citywalk", "bts", "mrt", "地铁", "车站", "攻略"]):
        modes.append("route")
    if any(x in compact for x in ["清单", "合集", "推荐", "避坑", "对比", "测评", "盘点", "一图"]):
        modes.append("bento")
    if any(x in compact for x in ["产品", "咖啡", "酒店", "餐厅", "品牌", "书店", "书籍", "设备", "耳机", "相机"]):
        modes.append("lifestyle")

    deduped: list[str] = []
    for mode in modes:
        if mode not in deduped:
            deduped.append(mode)
    return deduped[:5]


def extract_steps(markdown: str) -> list[str]:
    steps = []
    for line in markdown.splitlines():
        stripped = line.strip()
        match = re.match(r"^(?:\d+\.|[-*+])\s+(.+)$", stripped)
        if match:
            item = render_wechat_html.strip_inline_markdown(match.group(1))
            if item and len(item) <= 80:
                steps.append(item)
    return steps[:7]


def prompt_for_mode(mode: str, title: str, markdown: str, theme: str) -> str:
    text = plain_text(markdown)
    summary = " ".join(text.split())[:260]
    steps = extract_steps(markdown)
    if mode == "cover":
        return f"""Asset type: WeChat Official Account cover, 16:9 horizontal key visual
Article topic: {title}
Audience and mood: mobile WeChat readers; polished, useful, credible, visually memorable
Main visual: one strong concept drawn from the article, not generic decoration
Composition: wide editorial composition, strong focal point, generous clean space for platform crop
Style: {theme} adapted as premium editorial visual
Palette: 3-4 restrained colors matching the article body
Constraints: no readable text, no logos, no QR codes, no watermark, no fake UI text, no distorted hands or faces unless necessary
Article summary: {summary}"""
    if mode == "workflow":
        step_text = "; ".join(steps) if steps else "extract 4-6 key steps from the article"
        return f"""Asset type: Step-by-step workflow infographic
Topic: {title}
Steps: {step_text}
Layout: vertical-zigzag for mobile body image, clear numbered badges and connecting arrows
Style: clean friendly illustration, consistent icons, WeChat-readable labels
Palette: match the {theme} article theme
Constraints: step order obvious, each step visually consistent, no long text, no clutter"""
    if mode == "chat":
        return f"""Asset type: Mobile chat interface mockup for a WeChat article
Platform feel: clean AI assistant or WeChat-like mobile chat, light mode
Scenario: a short real-feeling conversation that demonstrates the article's core action
Participants: user and AI assistant
Messages: 6-8 short Chinese messages, each ideally under 35 characters
Style: high-fidelity clean mobile UI, readable Chinese text, calm spacing
Constraints: logical message order, no fake brand logos, no private data, no broken Chinese glyphs
Article topic: {title}"""
    if mode == "route":
        return f"""Asset type: Illustrated route map for a WeChat travel/guide article
Place or subject: infer from article title and source material
Route or stops: extract ordered stops from the article; keep labels short
Transport: infer from article, such as walk, BTS, MRT, taxi, high-speed rail, or mixed
Side panel: station tips, food highlights, or daily points
Style: elegant illustrated map, soft color, clear labels, mobile-readable
Constraints: route order correct, labels do not overlap, no false exact coordinates, no over-saturated tourist poster style
Article topic: {title}"""
    if mode == "bento":
        return f"""Asset type: Bento-grid infographic for a WeChat article
Topic: {title}
Modules: 6-9 concise modules extracted from the article
Hero module: the most useful recommendation, warning, or key number
Layout: asymmetric bento grid, aligned edges, consistent spacing, one large anchor module
Palette: limited palette matching {theme}; no more than 5 main colors
Style: polished editorial infographic, mobile-readable, not busy
Constraints: each module has a visual element, text kept short, no tiny unreadable paragraphs, no random icons"""
    return f"""Asset type: Lifestyle editorial scene for a WeChat article
Subject: the main product, tool, place, food, or object in "{title}"
Scene: realistic context where the subject is used or experienced
Lighting: natural soft light, coherent direction
Mood: polished, human, credible, aligned with {theme}
Composition: subject as focal point, shallow depth, clean negative space
Constraints: no fake logo, no readable invented packaging text, no clutter, no full-face person unless needed
Article summary: {summary}"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Plan cover/body images for a WeChat article.")
    parser.add_argument("markdown", type=Path)
    parser.add_argument("-o", "--output", type=Path, help="Output image-plan Markdown")
    parser.add_argument("--theme", choices=sorted([*render_wechat_html.THEMES, "auto"]), default="auto")
    parser.add_argument(
        "--mode",
        action="append",
        choices=sorted(MODE_LABELS),
        help="Force an image mode; may be repeated. Cover is always included.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.markdown.read_text(encoding="utf-8")
    meta, body = render_wechat_html.parse_frontmatter(source)
    title = render_wechat_html.extract_title(meta, body)
    theme, article_type = render_wechat_html.resolve_theme(args.theme, meta, body)
    modes = detect_modes(body, args.mode or [])
    output = args.output or args.markdown.with_name("image-plan.md")

    parts = [
        "# WeChat Image Plan",
        "",
        f"- Title: {title}",
        f"- Theme: {theme}",
        f"- Article type: {article_type}",
        f"- Modes: {', '.join(modes)}",
        "",
        "Use Codex's built-in image generation for generated assets. Use real/user-provided images where authenticity matters.",
        "",
    ]
    for index, mode in enumerate(modes, start=1):
        filename = "cover.png" if mode == "cover" else f"{index:02d}-{mode}.png"
        parts.extend(
            [
                f"## {index}. {MODE_LABELS[mode]}",
                "",
                f"- Suggested file: `assets/images/{filename}`",
                f"- Placement: {'cover' if mode == 'cover' else 'body image near the matching section'}",
                "",
                "```text",
                prompt_for_mode(mode, title, body, theme),
                "```",
                "",
            ]
        )

    output.write_text("\n".join(parts), encoding="utf-8")
    print(f"Wrote {output} (theme={theme}, article_type={article_type}, modes={','.join(modes)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
