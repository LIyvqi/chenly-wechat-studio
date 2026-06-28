# Chenly WeChat Studio

![Content-first WeChat article workflow](assets/readme-workflow.png)

宸旅公众号工坊是一个面向微信公众号文章生产的 Codex skill。它不只是把 Markdown 转成公众号 HTML，也不是一个固定模板转换器；更核心的用法是：

> 你用自然语言说清楚想写什么、给谁看、想达到什么效果，Codex 负责把它实现成一篇结构清楚、排版完整、适合微信公众号阅读的文章。

也就是说，这个 skill 同时覆盖内容实现、编辑改写、视觉方向选择、封面/配图规划、本地预览和可选的公众号草稿准备。

## What It Does

- 把一个想法、提纲、素材或口述需求整理成公众号文章。
- 对已有 Markdown 做结构优化、文风润色和公众号排版。
- 根据文章类型自动选择视觉方向，例如教程、产品发布、旅行攻略、复盘、观点、长文分析。
- 生成适合微信正文的 inline-styled HTML，而不是依赖本地网页壳的漂亮外观。
- 规划封面和正文图片：需要真实图片时提醒找图，需要概念图时可配合 Codex 图片生成。
- 默认只做本地 dry-run；只有明确要求提交时，才调用微信草稿相关流程。

## Two Main Ways To Use It

### 1. Content-first

你不需要先写 Markdown。可以直接告诉 Codex：

```text
Use $chenly-wechat-studio.

我想写一篇公众号文章，主题是“第一次用 AI 搭建公众号工作流”。
读者是想提高内容生产效率的个人创作者。
文章要有一点经验分享的温度，也要有清晰步骤。
请你帮我完成文章结构、正文、排版、封面方向和本地预览。
```

Codex 会先判断文章类型、读者意图、业务目标和审美方向，再决定是否需要重写、补结构、加模块、规划图片，最后用本地渲染器输出公众号 HTML。

### 2. Markdown-first

如果你已经有 Markdown，可以直接转换或进一步优化：

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/render_wechat_html.py article.md -o article.wechat.html --theme auto
```

需要仅复制正文片段：

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/render_wechat_html.py article.md -o article.fragment.html --fragment
```

需要检查提交到微信草稿的紧凑正文：

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/render_wechat_html.py article.md -o article.submitted.html --fragment --compact
```

## Typical Workflow

1. Tell Codex the article goal, audience, source material, tone, and any publishing constraints.
2. Codex classifies the article scene and chooses a visual direction.
3. Codex drafts or improves the Markdown structure when needed.
4. Codex plans cover/body images when images improve hook, explanation, proof, or rhythm.
5. The renderer creates WeChat-body-first HTML with inline styles.
6. For publishable drafts, Codex reviews body HTML, title length, digest, image paths, raw newlines, and empty paragraphs.

## Image Planning

For a low-manual image plan:

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/plan_wechat_images.py article.md --theme auto -o image-plan.md
```

Generated covers and conceptual body images should be saved beside the article, usually under `assets/images/`. Real products, places, routes, restaurants, hotels, interfaces, and factual claims should use user-provided or credible real images when authenticity matters.

## Draft Preparation

Dry-run draft payload:

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/submit_wechat_draft.py article.md --cover cover.png --theme auto
```

Real submission requires explicit intent plus WeChat credentials:

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/submit_wechat_draft.py article.md --cover cover.png --theme auto --submit
```

The real submit path uploads the cover, uploads local body images, rewrites image URLs, compacts submitted body HTML, and creates the WeChat draft.

## Examples

See [examples/README.md](examples/README.md) for copyable prompts that show the most important pattern: start from a loose idea or spoken brief, then let Codex implement the article and make the WeChat layout better.
