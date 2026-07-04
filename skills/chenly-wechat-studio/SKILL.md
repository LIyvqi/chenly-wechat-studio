---
name: chenly-wechat-studio
description: Create adaptive, aesthetically matched WeChat Official Account article drafts locally for Chenly/宸旅 with Codex, without md2wechat.cn API keys. Use when the user wants Markdown converted, rewritten, polished, previewed, exported as WeChat-ready HTML/CSS, automatically matched to a business/content scenario, or paired with a Codex-generated cover image, especially when they do not have MD2WECHAT_API_KEY or want Codex to generate the final article layout and cover directly instead of calling a remote conversion service.
---

# Chenly WeChat Studio

Use this skill for local WeChat Official Account article production. The core idea is:

1. Codex handles editorial judgment, rewriting, structure, and layout choices.
2. Codex chooses an aesthetic direction from the article's business scenario and reader intent.
3. The bundled renderer turns Markdown into WeChat-body-first, inline-styled HTML.
4. Codex's built-in image generation can create the cover image.
5. Codex plans or generates body images when images improve hook, explanation, proof, or reading rhythm.
6. No md2wechat.cn API key is required.

Do not call `md2wechat convert` in API mode. Do not request `MD2WECHAT_API_KEY`. Do not upload images or create drafts unless the user explicitly asks to push/submit/create a WeChat draft.

## WeChat Reality Check

Optimize the article body, not the local preview shell.

- WeChat drafts receive the submitted body HTML. The local `<main>`, `<article>`, page background, outer shadow, and preview header may not survive in the official editor.
- Avoid relying on full-page web layout polish. Make the body itself beautiful: opening lead, images, headings, rhythm, cards, quotes, and final note.
- Before creating a draft, compact the body HTML so raw newlines between tags do not become empty paragraphs in WeChat.
- Avoid English template labels such as `EDITOR'S NOTE`, `SECTION`, `WECHAT DRAFT` in the submitted body unless the article intentionally uses English. Prefer Chinese labels or no label.
- Local body image paths must be uploaded and rewritten before a real draft is created. The cover upload alone is not enough.

## Workflow

1. Read the source Markdown and any brand/profile instructions the user provides.
2. Keep the original Markdown read-only unless the user asks to edit it.
3. For substantial work, create a small working folder with `source.md`, optional `plan.md`, `review.md`, and `build/` outputs.
4. Classify the article before styling: article type, target reader, business goal, visual direction, layout modules, cover direction.
5. If images matter, read `references/image-playbook.md`. For user-supplied image sets, use the fast path below; for sourced or generated images, create an image plan with source strategy, prompts, target file names, and article placement.
6. If the article needs improvement, create a temporary or sibling Markdown draft with Codex-authored edits and only add visual modules that clarify the content.
7. If the user needs a cover and no cover is supplied, use Codex's built-in `image_gen` capability to generate a 16:9 raster cover, save it beside the article as `cover.png`, and keep the prompt in the working folder.
8. Render the final Markdown with `scripts/render_wechat_html.py`; prefer `--theme auto` unless the user names a specific direction.
9. For publishable drafts, review the submitted body HTML, not only the full preview page: title length, digest length, cover present, theme fit, opening rhythm, body image URLs, raw newline count, empty paragraphs, and WeChat credentials/IP readiness.
10. Return the cover path, output HTML path, selected theme, inferred article type, image plan/generated image paths, and a short note about any limitations.

## Self-Evolution And Repo Sync

Treat the installed skill at `~/.codex/skills/chenly-wechat-studio` as the working copy used in real publishing. When this installed skill is improved during actual use, mirror the same skill files back to the source repository at `chenly-wechat-studio/skills/chenly-wechat-studio` before considering the improvement done.

Do not sync or commit account secrets, tokens, uploaded media IDs, draft payloads, local `.env` files, or private WeChat configuration. Documentation may mention credential requirements generically, but real `WECHAT_APPID`, `WECHAT_SECRET`, access tokens, draft JSON, and image upload records must stay out of the repository.

## Fast Path for Supplied Images

Use this when the user already attached screenshots/photos/final posters and asks to create or push a draft quickly.

1. Treat user-provided images as the source of truth. Do not browse for replacements or generate new body images unless the user asks.
2. Batch copy and rename images into `assets/images/` in one shell command. Inspect dimensions in one `file` or `sips -g pixelWidth -g pixelHeight` call instead of opening every image visually.
3. Choose a cover quickly: use an explicitly supplied cover, a supplied 16:9 image, or crop the strongest final-result image to 16:9 with `sips -c <height> <width>`. Generate a cover only when supplied images cannot make a credible cover.
4. Put all requested images into the Markdown body in the promised order. Add one short sentence or caption around each image explaining its job; avoid long image-analysis prose.
5. Dry-run once with `submit_wechat_draft.py` without `--submit`. If `empty_paragraph_count` and `raw_newline_count` are `0`, submit immediately; let the submit script upload and rewrite body image URLs.
6. Write only a short `image-plan.md` after submission when useful for reuse. Do not block a simple push on a long pre-plan.

Recommended command:

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/render_wechat_html.py article.md -o article.wechat.html --theme auto
```

Use `--fragment` when the user wants only the copyable article body instead of a full preview page:

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/render_wechat_html.py article.md -o article.fragment.html --fragment
```

Use `--compact` when checking the exact body shape that should be submitted to WeChat:

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/render_wechat_html.py article.md -o article.submitted.html --fragment --compact
```

For a low-manual workflow that prepares a WeChat draft payload:

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/submit_wechat_draft.py article.md --cover cover.jpg --theme auto
```

For a low-manual image plan before generating or sourcing pictures:

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/plan_wechat_images.py article.md --theme auto -o image-plan.md
```

That command is dry-run by default. It writes preview HTML, article-body HTML, and `draft.json` without touching WeChat. To create a real WeChat draft after credentials are configured:

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/submit_wechat_draft.py article.md --cover cover.jpg --theme auto --submit
```

`--submit` uploads the cover image, uploads local body images, rewrites body image `src` values to WeChat URLs, compacts the submitted body HTML, and creates the draft with `md2wechat create_draft`. It requires WeChat Official Account `WECHAT_APPID` and `WECHAT_SECRET` or equivalent config. It does not require `MD2WECHAT_API_KEY` for a direct single-account config.

The submit script writes both a human preview and the exact body used for the draft:

- `*.wechat.html`: local full-page preview only.
- `*.body.html`: readable body HTML before upload/compaction.
- `*.submitted.body.html`: exact compact body inserted into the draft payload.
- `*.draft.json`: final draft payload.
- `*.image-uploads.json`: local-to-WeChat body image map, when body images are uploaded.

## Cover Generation

Use Codex's built-in image generation for covers and conceptual body images instead of `md2wechat generate_cover`, because `md2wechat generate_cover` requires an external image provider key and may upload to WeChat. For real products, places, restaurants, hotels, routes, and interfaces, prefer user-provided or sourced real images when authenticity matters.

Default cover prompt pattern:

```text
Use case: ads-marketing
Asset type: WeChat Official Account article cover, 16:9 horizontal banner
Primary request: a polished editorial cover for <article title and topic>
Style/medium: premium editorial illustration or clean product-design visual
Composition/framing: wide 16:9 composition, clear focal point, generous margins, suitable for public-account cover crop
Text (verbatim): no text inside the image
Constraints: no readable text, no logos, no QR codes, no watermarks, no brand marks, no human faces unless the article explicitly needs them
```

After generation, copy the selected image into the article folder:

```bash
cp ~/.codex/generated_images/<run>/<image>.png ./cover.png
```

Use that cover in the submit flow:

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/submit_wechat_draft.py article.md --cover cover.png --theme auto --submit
```

## Body Image Generation

Read `references/image-playbook.md` when the user asks for prettier images, better visual rhythm, "真实美丽的图片", "找图也可以生成", or when the article naturally needs explanatory visuals.

Use these core image modes:

- editorial cover / key visual: the default first visual.
- bento infographic: recommendations, comparisons, guides, "一图讲清".
- step/workflow graphic: tutorials, process stories, AI publishing flows.
- chat/AI conversation mockup: prompt/result stories and dialogue.
- route/map/travel graphic: travel, transit, city walk, station guides.
- product/lifestyle scene: tools, products, food, venues, desks, objects.

For generated assets, keep the prompt visible in `image-plan.md` or `assets/prompts/`. For sourced real images, record source URLs and avoid pretending generated images are real photos.

## Theme Choice

Default to `--theme auto`. It uses frontmatter first, then content signals:

```yaml
---
article_type: tutorial
visual_direction: clear-engineering
---
```

Use a named theme only when the user asks for a specific visual direction. Choose from:

- `clean-tech`: technical articles, tools, product notes, tutorials.
- `warm-editorial`: essays, personal reflections, narrative posts.
- `minimal-ink`: serious analysis, newsletters, longform writing.
- `wechat-green`: conservative WeChat-native feel.
- `press-card`: report, review, announcement, serious creator update.
- `tufte-ink`: reflective longform, conceptual explanation, quiet essay.
- `magazine-editorial`: deep analysis, interviews, strategy writing.
- `newspaper-press`: news, timely commentary, press-style updates.
- `swiss-product`: product launches, feature notes, modern tool articles.
- `ink-literary`: literary, cultural, quiet reflective prose.
- `bold-opinion`: strong opinion, critique, sharper arguments.

If unsure, use `clean-tech` for technical/work content and `warm-editorial` for personal/public-account essays.

## Adaptive Aesthetic Harness

Read `references/aesthetic-system.md` when the user asks for stronger aesthetics, multiple business scenes, "高级感", "取百家之长", or when the article type is not obvious.

Borrow the spirit of beautiful web-article harnesses without turning this skill into a React project:

- Treat the first screen as the most important spread: title, digest, opening lead, first image, and first section must feel intentional.
- Before choosing a visual system, answer four questions: narrative role, viewing distance, visual temperature, and capacity fit.
- Convert the first paragraph into a lead note when it can carry the article promise.
- Use a few strong visual blocks instead of many decorations: lead, section cards, quote blocks, step/list cards, code panels.
- Prefer restrained editorial contrast: one accent color, one soft surface color, generous spacing, and mobile-readable line height.
- Preserve WeChat editor compatibility: inline styles, no external fonts, no scripts, no fragile grid/app layouts, and no important styling that only exists in the preview shell.
- If doing a major rewrite, write `plan.md` first with: article type, target reader, structure, theme, cover direction, and submit decision.
- Choose modules from content shape, not taste alone: tutorial steps, product feature cards, analysis quotes, dialogue blocks, stat blocks, or warnings.
- For substantial visual work, create a small first-spread preview early: opening lead, first image, first heading, and one representative module. Judge the direction before polishing the whole article.

## Codex Layout Layer

Before rendering, Codex may improve the Markdown using simple, honest structure:

- Add a short opening hook when the article starts abruptly.
- Split long sections with `##` headings.
- Convert dense lists into short paragraphs or bullet groups.
- Add a concise conclusion or call to action only if the article supports it.
- Avoid fake data, fake quotes, fake citations, and unsupported claims.

Keep WeChat mobile reading in mind: short paragraphs, clear headings, beautiful images, no deeply nested lists, and minimal tables.

## Pre-Submit Review

For real WeChat drafts, check the `*.submitted.body.html` and `*.draft.json` outputs:

- `raw_newline_count` should be `0` or very low.
- `empty_paragraph_count` should be `0`.
- `remaining_local_images` should be empty.
- Body screenshots should feel good without relying on the local preview background or outer card.
- If the article looks worse in the published page than local preview, simplify body modules first: fewer card borders, stronger images, cleaner headings, and more natural Chinese labels.

## Renderer Notes

The renderer supports common Markdown:

- frontmatter `title`, `author`, `digest`
- headings, paragraphs, bold, italic, inline code, links
- blockquotes, fenced code blocks, lists, images, horizontal rules
- simple pipe tables
- callouts using `> [!tip]`, `> [!important]`, `> [!warning]`, `> [!note]`
- containers using `:::stat[Label]`, `:::dialogue[Title]`, `:::gallery[Title]`, `:::byline[Name]`
- inline highlights using `==important phrase==`

The renderer is intentionally local and deterministic. It adds editorial styling for the opening lead, section headings, quote blocks, callouts, list cards, data blocks, dialogue blocks, code panels, and tables. The standalone renderer preserves image paths. The submit script uploads and rewrites local body images when `--submit` is used.

Read `references/style-guide.md` when the user asks for article rewriting, voice design, or a stronger editorial pass.
