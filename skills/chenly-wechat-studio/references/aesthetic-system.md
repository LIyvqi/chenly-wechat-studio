# Adaptive WeChat Aesthetic System

Use this reference when the user wants a publishable WeChat article whose layout should fit the business, content type, and account tone instead of using a fixed template.

## Core Principle

Beauty is fit. Choose the visual language from the article's job:

- What is the reader trying to do after reading?
- Is the article teaching, announcing, persuading, reflecting, reporting, or interviewing?
- Should the reader feel clarity, trust, momentum, warmth, authority, or taste?
- Which elements clarify the content, and which are decorative noise?

Do not ask the user to pick a theme when the content gives enough signal. Infer a direction, state it briefly, and render a preview.

Before picking modules or images, answer four design questions:

- Narrative role: hook, explanation, proof, rest, or closing?
- Viewing distance: phone reading at 10-30cm, so labels and body text must survive mobile size.
- Visual temperature: quiet, energized, authoritative, warm, premium, playful, or practical?
- Capacity fit: does the content fit the intended block, or will it become cramped or empty?

## Scene Router

| Scene | Use When | Visual Direction | Default Theme | Best Modules |
| --- | --- | --- | --- | --- |
| `tutorial` | steps, setup, CLI/API, code, how-to | clear engineering | `clean-tech` | lead, ordered steps, code panels, warning callout |
| `product` | product launch, feature notes, tool intro | modern product editorial | `swiss-product` | lead, feature cards, stat, comparison table |
| `analysis` | trend, strategy, long argument, research | magazine editorial | `magazine-editorial` | lead, section cards, quote, table |
| `news` | hot event, update, quick read | press/newsroom | `newspaper-press` | strong section headings, quote, bullets |
| `essay` | personal view, creator reflection, narrative | warm human editorial | `warm-editorial` | lead, soft quote, sparse lists |
| `interview` | dialogue, Q&A, conversation | interview magazine | `magazine-editorial` | dialogue, quote, byline |
| `case-study` | project review, failure, growth, before/after | structured report | `press-card` | timeline-like steps, table, important callout |
| `listicle` | checklist, tools, recommendations | scan-friendly cards | `wechat-green` | list cards, tip callout, separators |
| `literary` | culture, reading, art, reflective prose | quiet ink | `ink-literary` | lead, plain headings, quote |
| `opinion` | strong stance, critique, hot take | bold opinion | `bold-opinion` | lead, punchy headings, important callout |

## Image Router

Read `image-playbook.md` before generating or sourcing images. Use body images only when they improve hook, explanation, proof, rest, or delight.

| Content Need | Recommended Image Mode | Notes |
| --- | --- | --- |
| first impression / cover | editorial cover / key visual | 16:9, text-free, one strong subject |
| multiple dimensions / comparison | bento infographic | 6-9 modules, one anchor module |
| tutorial / process / AI workflow | step/workflow graphic | 3-7 steps, clear order |
| prompt / AI conversation / interview | chat mockup | 6-10 short messages |
| travel / transit / route | route/map graphic | real references for factual routes |
| product / place / object | product/lifestyle scene | real images if recognition matters |

## Visual Directions

- `clear engineering`: high legibility, code-friendly, cool accent, practical blocks.
- `modern product editorial`: grid feeling, strong contrast, controlled cards, concise feature hierarchy.
- `magazine editorial`: generous spacing, calm authority, strong opening spread, restrained decorative labels.
- `press/newsroom`: compact, serious, headline-driven, quote and fact blocks.
- `warm human editorial`: warmer surface, softer cards, fewer hard edges, good for founder notes and personal essays.
- `quiet ink`: minimal color, literary rhythm, quote emphasis, very little decoration.
- `bold opinion`: stronger accent, high contrast section starts, but avoid poster-like overload.

## Content Element Decisions

Use special containers only when they clarify the article.

| Content Shape | Markdown Element | Boundary |
| --- | --- | --- |
| Key judgment or contrarian idea | `> [!important] Title` | 1-2 per article |
| Practical tip | `> [!tip] Title` | 0-2 per article |
| Risk or limitation | `> [!warning] Title` | only for real risk |
| Background note | `> [!note] Title` | delete if not useful |
| Article-level number | `:::stat[Label]` | 0-1 per article |
| Interview/dialogue | `:::dialogue[Title]` | only actual dialogue |
| Image sequence | `:::gallery[Title]` | 3+ images |
| Author closing note | `:::byline[Name]` | 0-1 at the end |
| Important phrase | `==highlight==` | no more than 5 |
| Contrast phrase | `~~old~~ new` | no more than 2 |

Container syntax:

```markdown
:::stat[核心数据]
3 分钟
从 Markdown 到公众号草稿箱的最短人工路径。
:::

:::dialogue[一次真实对话]
我：这个流程能自动提交吗？
Codex：可以，但要先处理 AppSecret 和 IP 白名单。
:::
```

## Anti-Decoration Check

Before final rendering, ask:

- If this block is removed, does the reader lose meaning?
- Are there more than 3 consecutive blocks with the same shape?
- Are there too many callouts, highlights, or cards?
- Does the first screen communicate why the article matters?
- Is the cover using the same aesthetic direction as the body?
- Does every generated image have a job, and would the article be worse without it?

## Cover Direction

Match the cover to the selected direction:

- tutorial: product UI, workflow diagram feeling, clean technical composition.
- product: polished product scene, abstract interface layers, crisp contrast.
- analysis/news: editorial cover, newspaper/magazine sensibility, fewer icons.
- essay/literary: restrained still life, soft light, no literal clutter.
- opinion: bold single focal point, strong contrast, no fake text.

Keep cover images text-free unless the user explicitly asks for title text.

## WeChat Typography Baseline

Use these as renderer/editorial defaults unless the theme has a strong reason to differ:

- Body text: 15-16px, not pure black; prefer #3f3f3f / #4a4a4a / theme text colors.
- Line height: 1.75-1.9 for mobile long reading.
- Paragraph spacing: enough to breathe, but not so much that related thoughts disconnect.
- Colors: outside images, keep body colors to one text color, one accent color, and one muted note color.
- Emphasis: prefer bold/color/callout; avoid Chinese italics and avoid underlines except links.
- Alignment: left alignment for deep reading and guides; center alignment only for short entertainment, poster, or slogan moments.
