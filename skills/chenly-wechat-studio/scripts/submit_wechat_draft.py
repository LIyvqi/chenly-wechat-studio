#!/usr/bin/env python3
"""Prepare or submit a WeChat draft from Markdown without md2wechat API mode."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path
from typing import Any

import render_wechat_html


def first_non_empty(*values: str | None) -> str:
    for value in values:
        if value:
            value = value.strip()
            if value:
                return value
    return ""


def plain_digest(markdown: str, limit: int = 120) -> str:
    text = render_wechat_html.strip_inline_markdown(markdown)
    lines = []
    in_code = False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            in_code = not in_code
            continue
        if in_code or not line:
            continue
        if line.startswith("#"):
            continue
        if line.startswith((">", "-", "*", "+")):
            line = line[1:].strip()
        lines.append(line)
    digest = " ".join(" ".join(lines).split())
    if len(digest) > limit:
        digest = digest[:limit] + "..."
    return digest


def find_key(obj: Any, key: str) -> Any:
    if isinstance(obj, dict):
        if key in obj:
            return obj[key]
        for value in obj.values():
            found = find_key(value, key)
            if found:
                return found
    elif isinstance(obj, list):
        for value in obj:
            found = find_key(value, key)
            if found:
                return found
    return None


def run_json(cmd: list[str]) -> dict[str, Any]:
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if proc.returncode != 0:
        message = proc.stderr.strip() or proc.stdout.strip() or f"command failed: {' '.join(cmd)}"
        raise RuntimeError(message)
    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"command did not return JSON: {' '.join(cmd)}\n{proc.stdout}") from exc


def upload_image(image: Path, wechat_account: str) -> dict[str, str]:
    cmd = ["md2wechat", "upload_image", str(image), "--json"]
    if wechat_account:
        cmd.extend(["--wechat-account", wechat_account])
    response = run_json(cmd)
    media_id = find_key(response, "media_id")
    url = find_key(response, "wechat_url") or find_key(response, "url")
    if not media_id:
        raise RuntimeError(f"upload_image did not return media_id: {response}")
    return {"media_id": str(media_id), "url": str(url or "")}


def upload_cover(cover: Path, wechat_account: str) -> str:
    return upload_image(cover, wechat_account)["media_id"]


def is_remote_src(src: str) -> bool:
    return src.startswith(("http://", "https://", "data:"))


def resolve_image_path(src: str, source_dir: Path) -> Path:
    path = Path(src)
    if not path.is_absolute():
        path = source_dir / path
    return path


def local_image_sources(article_html: str) -> list[str]:
    sources = []
    for match in re.finditer(r'<img\b[^>]*\bsrc=(["\'])(.*?)\1', article_html, re.IGNORECASE):
        src = match.group(2)
        if src and not is_remote_src(src):
            sources.append(src)
    return sources


def upload_body_images(article_html: str, source_dir: Path, wechat_account: str) -> tuple[str, dict[str, str]]:
    uploads: dict[str, str] = {}

    def replace_src(match: re.Match[str]) -> str:
        quote = match.group(1)
        src = match.group(2)
        if is_remote_src(src):
            return match.group(0)
        if src in uploads:
            target_url = uploads[src]
        else:
            image_path = resolve_image_path(src, source_dir)
            if not image_path.exists():
                raise RuntimeError(f"body image not found: {src} resolved to {image_path}")
            uploaded = upload_image(image_path, wechat_account)
            target_url = uploaded["url"]
            if not target_url:
                raise RuntimeError(f"upload_image did not return url for body image: {src}")
            uploads[src] = target_url
        return match.group(0).replace(f"src={quote}{src}{quote}", f"src={quote}{target_url}{quote}", 1)

    updated = re.sub(r'<img\b[^>]*\bsrc=(["\'])(.*?)\1', replace_src, article_html, flags=re.IGNORECASE)
    return updated, uploads


def create_draft(draft_json: Path, wechat_account: str) -> dict[str, Any]:
    cmd = ["md2wechat", "create_draft", str(draft_json), "--json"]
    if wechat_account:
        cmd.extend(["--wechat-account", wechat_account])
    return run_json(cmd)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare or submit a WeChat draft from Markdown.")
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--cover", type=Path, help="Local cover image to upload when --submit is used")
    parser.add_argument("--cover-media-id", help="Existing WeChat permanent material media_id")
    parser.add_argument("--theme", choices=sorted([*render_wechat_html.THEMES, "auto"]), default="auto")
    parser.add_argument("--title", help="Override draft title")
    parser.add_argument("--author", help="Override draft author")
    parser.add_argument("--digest", help="Override draft digest")
    parser.add_argument("--output-dir", type=Path, help="Directory for generated artifacts")
    parser.add_argument("--wechat-account", help="Named WeChat account from md2wechat config")
    parser.add_argument("--submit", action="store_true", help="Upload cover and create the WeChat draft")
    parser.add_argument(
        "--no-upload-body-images",
        action="store_true",
        help="Do not upload local body images during --submit",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.cover and args.cover_media_id:
        raise SystemExit("--cover and --cover-media-id are mutually exclusive")
    if args.submit and not args.cover and not args.cover_media_id:
        raise SystemExit("--submit requires --cover or --cover-media-id")

    source_text = args.markdown.read_text(encoding="utf-8")
    meta, body = render_wechat_html.parse_frontmatter(source_text)
    title = first_non_empty(args.title, meta.get("title"), render_wechat_html.extract_title(meta, body))
    author = first_non_empty(args.author, meta.get("author"))
    digest = first_non_empty(
        args.digest,
        meta.get("digest"),
        meta.get("summary"),
        meta.get("description"),
        plain_digest(body),
    )

    out_dir = args.output_dir or args.markdown.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = args.markdown.stem
    preview_html = out_dir / f"{stem}.wechat.html"
    body_html = out_dir / f"{stem}.body.html"
    submitted_body_html = out_dir / f"{stem}.submitted.body.html"
    image_uploads_json = out_dir / f"{stem}.image-uploads.json"
    draft_json = out_dir / f"{stem}.draft.json"

    resolved_theme, article_type = render_wechat_html.resolve_theme(args.theme, meta, body)
    article_html = render_wechat_html.render_markdown(body, resolved_theme, document_title=title, meta=meta)
    full_page = render_wechat_html.build_full_page(
        article_html,
        title,
        {**meta, "author": author, "digest": digest},
        resolved_theme,
    )
    preview_html.write_text(full_page, encoding="utf-8")
    body_html.write_text(article_html, encoding="utf-8")

    cover_media_id = args.cover_media_id or ""
    if args.submit and args.cover:
        cover_media_id = upload_cover(args.cover, args.wechat_account or "")

    submitted_html = article_html
    image_uploads: dict[str, str] = {}
    if args.submit and not args.no_upload_body_images:
        submitted_html, image_uploads = upload_body_images(submitted_html, args.markdown.parent, args.wechat_account or "")
        image_uploads_json.write_text(json.dumps(image_uploads, ensure_ascii=False, indent=2), encoding="utf-8")

    submitted_html = render_wechat_html.compact_wechat_html(submitted_html)
    submitted_body_html.write_text(submitted_html, encoding="utf-8")
    remaining_local_images = local_image_sources(submitted_html)
    if args.submit and remaining_local_images and not args.no_upload_body_images:
        raise RuntimeError(f"local body images remain after upload: {remaining_local_images}")

    payload = {
        "articles": [
            {
                "title": title[:32],
                "author": author[:16],
                "digest": digest[:128],
                "content": submitted_html,
                "thumb_media_id": cover_media_id,
                "show_cover_pic": 1 if cover_media_id else 0,
            }
        ]
    }
    draft_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    result: dict[str, Any] | None = None
    if args.submit:
        result = create_draft(draft_json, args.wechat_account or "")

    summary = {
        "preview_html": str(preview_html),
        "body_html": str(body_html),
        "submitted_body_html": str(submitted_body_html),
        "draft_json": str(draft_json),
        "submitted": bool(args.submit),
        "theme": resolved_theme,
        "article_type": article_type,
        "cover_media_id": cover_media_id,
        "image_uploads": image_uploads,
        "remaining_local_images": remaining_local_images,
        "empty_paragraph_count": len(re.findall(r"<p[^>]*>\s*</p>", submitted_html)),
        "raw_newline_count": submitted_html.count("\n"),
        "result": result,
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
