# WeChat Image Playbook

Use this reference when a WeChat article needs a cover, body illustrations, explainers, UI mockups, travel visuals, or more beautiful image rhythm.

This playbook adapts the useful parts of ConardLi/garden-skills `gpt-image-2`, `beautiful-article`, and `web-design-engineer` for WeChat Official Account articles. Keep the output WeChat-native: raster images, simple inline HTML, no React dependency, no fragile web layout.

## Image Principle

Images must do at least one real job:

- Hook: make the first screen worth stopping on.
- Explain: show a map, flow, comparison, process, product, UI, or before/after.
- Rest: break dense text and give the reader a visual pause.
- Prove: use real screenshots, real product/place photos, or sourced references when truth matters.
- Delight: add taste, but only when it matches the article.

Do not add generic decorative pictures. A beautiful but irrelevant picture weakens the article.

## Source Strategy

Choose the source in this order:

1. User-provided screenshots/photos when authenticity matters.
2. Real web images from official or credible sources when the subject is a real product, place, person, venue, route, food, or interface.
3. Generated images for covers, conceptual explainers, process graphics, editorial illustrations, non-literal metaphors, and anonymized UI mockups.
4. Simple HTML/CSS modules when text is clearer than an image.

If using web images, record source URLs in `review.md` or `image-plan.md`. Avoid copyrighted full-resolution reuse when rights are unclear; prefer official press images, user-supplied assets, generated visuals, or images with clear usage terms.

## Core Image Modes

### 1. Editorial Cover / Key Visual

Use for: almost every article, especially essays, product notes, AI workflow posts, analysis, and travel guides.

Default output:

- 16:9 horizontal cover for WeChat cover crop.
- No readable text inside the image unless the user explicitly asks.
- One strong subject, clear negative space, coherent palette with the article theme.

Prompt structure:

```text
Asset type: WeChat Official Account cover, 16:9 horizontal key visual
Article topic: <topic>
Audience and mood: <reader + desired feeling>
Main visual: <single subject or concept>
Composition: wide editorial composition, strong focal point, generous clean space for platform crop
Style: <magazine / premium product / warm editorial / clean technical / travel editorial>
Palette: <3-4 colors matching the article theme>
Constraints: no readable text, no logos, no QR codes, no watermark, no fake UI text, no distorted hands or faces unless necessary
```

### 2. Bento / High-Density Information Graphic

Use for: guides, recommendations, comparisons, "one picture explains it", shopping lists, tool roundups, travel cheat sheets.

Default output:

- 3:4 portrait for body image or 16:9 if it must sit near the top.
- 6-9 modules, one large anchor module, consistent rounded rectangles and gaps.
- Use when a single article section contains multiple dimensions.

Prompt structure:

```text
Asset type: Bento-grid infographic for a WeChat article
Topic: <topic>
Modules: <6-9 module titles>
Hero module: <the largest / most important item>
Layout: asymmetric bento grid, aligned edges, consistent spacing
Palette: <limited palette, no more than 5 main colors>
Style: polished editorial infographic, mobile-readable, not busy
Constraints: each module has a visual element, text kept short, no tiny unreadable paragraphs, no random icons
```

### 3. Step / Workflow Graphic

Use for: tutorials, "I did four steps", recipes, AI workflow demonstrations, publishing processes.

Default output:

- 3-7 steps, max 9.
- Each step gets a number, short title, small illustration/icon, and connection line/arrow.
- For technical content, keep the drawing warm and clear rather than engineering-heavy unless the article is explicitly technical.

Prompt structure:

```text
Asset type: Step-by-step workflow infographic
Topic: <workflow topic>
Steps: <numbered steps with 4-8 character titles and 1-line descriptions>
Layout: vertical-zigzag for mobile body image, or horizontal-row for 16:9 cover
Style: clean friendly illustration, consistent icons, clear numbered badges
Palette: <theme colors>
Constraints: step order must be obvious, each step visually consistent, no long text, no clutter
```

### 4. Chat / AI Conversation Mockup

Use for: AI prompts, one-sentence-to-output stories, customer service examples, interview/dialogue articles.

Default output:

- Mobile chat screenshot feel, but clearly a designed mockup if factual risk exists.
- 6-10 messages, realistic timestamps, clean bubbles.
- Good for showing "what I said to AI" and "what AI returned".

Prompt structure:

```text
Asset type: Mobile chat interface mockup for a WeChat article
Platform feel: WeChat-like / AI assistant / generic mobile chat
Scenario: <conversation context>
Participants: <names/roles>
Messages: <6-10 short messages, each under 35 Chinese characters when possible>
Style: high-fidelity clean mobile UI, readable Chinese text, light mode
Constraints: message order logical, no fake brand logos, no private data, no broken Chinese glyphs
```

### 5. Route / Map / Travel Guide Graphic

Use for: travel posts, city walks, food routes, transit guides, station-by-station articles.

Default output:

- Real geography should be directionally plausible, but not a survey-grade map.
- Label only the useful stops. Avoid label collisions.
- Use real screenshots/map references when factual precision matters; generate illustrated overlays for beauty.

Prompt structure:

```text
Asset type: Illustrated route map for a WeChat travel guide
Place: <city/area>
Route or stops: <ordered stops>
Transport: <BTS/MRT/walk/taxi/high-speed rail/etc.>
Side panel: <daily points / station tips / food highlights>
Style: elegant illustrated map, soft color, clear labels, mobile-readable
Constraints: route order correct, labels do not overlap, no false exact coordinates, no over-saturated tourist poster style
```

### 6. Product / Lifestyle Scene

Use for: tools, products, consumer goods, books, devices, creator desk setups, cafe/food recommendations.

Default output:

- One product or scene as the focal point.
- Natural light, real usage context, minimal props.
- Use real product imagery if brand recognition matters.

Prompt structure:

```text
Asset type: Lifestyle editorial scene for a WeChat article
Subject: <product/place/object>
Scene: <desk/cafe/travel/studio/kitchen/etc.>
Lighting: natural soft light, coherent direction
Mood: <professional/warm/premium/human/travel>
Composition: subject as focal point, shallow depth, clean negative space
Constraints: no fake logo, no readable invented packaging text, no clutter, no person face unless needed
```

## GPT Image Workflow

When generating images with Codex's built-in image capability:

1. Write an `image-plan.md` first for substantial articles: image purpose, source strategy, prompt, expected file name, and placement.
2. Use generated images for covers and conceptual/body visuals. Use real images/screenshots where authenticity matters.
3. Save prompts beside the article in `assets/prompts/` or include them in `image-plan.md`.
4. Save outputs under `assets/images/` with semantic names such as `cover.png`, `workflow-steps.png`, `route-map.png`.
5. Insert generated/body images into Markdown with useful alt text.
6. Before `--submit`, ensure local body images will be uploaded by `submit_wechat_draft.py`.

## Ratio Guide

- WeChat cover: 16:9 horizontal, text-free.
- First body visual: 16:9 or 4:3 if it is a screenshot; 3:4 if it is an infographic.
- Process / travel / bento body visual: 3:4 portrait for mobile readability.
- Chat mockup: 9:16 or tall portrait.
- Product / lifestyle scene: 4:3, 3:4, or 16:9 depending on placement.

## Visual QA

Before final submission:

- Squint test: is there one obvious focal point?
- Mobile test: can labels be read on a phone?
- Purpose test: if removed, does the article lose meaning, trust, or rhythm?
- Palette test: does the image match the article theme instead of fighting it?
- Authenticity test: are real-world claims supported by real sources, screenshots, or safe generated concepts?
- WeChat test: body images are local before dry-run and uploaded/replaced before real submit.

## Research Notes

External WeChat layout research distilled here:

- 365 Editor emphasizes that typography should reduce reader pressure, improve logic tracking, and give readers rest; it recommends limited color use and mobile-friendly text sizing/spacing.
- Product/operation design writing repeatedly stresses that images should explain, create rest, or support credibility rather than act as random decoration.
- Editor/tool guides converge on consistency, adequate spacing, restrained style variation, and brand/color coherence.

