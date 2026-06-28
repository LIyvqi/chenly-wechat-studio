# Chenly WeChat Studio

Adaptive WeChat Official Account article production for Codex.

`chenly-wechat-studio` turns Markdown into polished WeChat-ready drafts with:

- adaptive article-type and aesthetic selection
- WeChat-body-first inline HTML rendering
- cover and body-image planning
- optional Codex-generated visuals
- dry-run draft payload generation
- optional WeChat draft submission through local `md2wechat` CLI

It does **not** require an `MD2WECHAT_API_KEY` or the md2wechat.cn conversion API.

## Install

Manual install:

```bash
mkdir -p ~/.codex/skills
cp -R skills/chenly-wechat-studio ~/.codex/skills/chenly-wechat-studio
```

Or ask Codex to install the skill from this GitHub repo path:

```text
Install the skill from https://github.com/<owner>/<repo>/tree/main/skills/chenly-wechat-studio
```

Restart Codex after installing so the new skill is discovered.

## Usage

Render a local preview:

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/render_wechat_html.py article.md -o article.wechat.html --theme auto
```

Render the exact body fragment shape:

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/render_wechat_html.py article.md -o article.submitted.html --fragment --compact --theme auto
```

Prepare a dry-run WeChat draft payload:

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/submit_wechat_draft.py article.md --cover cover.png --theme auto
```

Create a real WeChat draft after local WeChat credentials and IP whitelist are configured:

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/submit_wechat_draft.py article.md --cover cover.png --theme auto --submit
```

## Article Frontmatter

```yaml
---
title: "Your article title"
author: "Your name"
digest: "Short WeChat digest"
article_type: tutorial
visual_direction: clear-engineering
---
```

`--theme auto` can infer a theme from content, but frontmatter gives it stronger editorial intent.

## Real WeChat Submission

Real draft creation uses the local `md2wechat` CLI for WeChat API operations only:

- upload cover image
- upload local body images
- create WeChat draft

Keep credentials outside the repository. Use environment variables or local config:

```bash
export WECHAT_APPID="your_appid"
export WECHAT_SECRET="your_appsecret"
```

Never commit AppID/AppSecret, access tokens, draft payloads containing private media IDs, or local config files.

## Repository Layout

```text
.
├── README.md
├── LICENSE
├── examples/
│   └── article.md
└── skills/
    └── chenly-wechat-studio/
        ├── SKILL.md
        ├── agents/openai.yaml
        ├── references/
        └── scripts/
```

## License

MIT.
