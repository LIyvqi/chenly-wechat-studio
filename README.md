# Chenly WeChat Studio

`chenly-wechat-studio` 是一个面向 Codex 的公众号文章生产 Skill。

它不是简单的 Markdown 转 HTML 工具，而是一套更接近“公众号编辑工作室”的本地工作流：Codex 负责文章判断、结构优化、审美选择、封面与正文图片规划；本地脚本负责把 Markdown 渲染成微信正文优先的内联 HTML，并在需要时准备或提交公众号草稿。

这个项目最初为“宸旅公众号工坊”而写，但并不限定只能写旅行内容。它适合技术教程、产品介绍、个人随笔、深度分析、热点评论、项目复盘、清单干货、访谈对话等不同类型的公众号文章。

## 它能做什么

- 根据文章内容自动判断文章类型和视觉方向。
- 把 Markdown 渲染成适合公众号正文的内联 HTML。
- 支持封面图和正文图片规划。
- 支持 Codex 生成封面图或概念配图。
- 支持 dry-run，先生成预览 HTML、正文 HTML 和草稿 JSON。
- 支持真实提交到微信公众号草稿箱。
- 不依赖 `MD2WECHAT_API_KEY`，不需要 md2wechat.cn 转换接口。

## 设计理念

公众号排版不应该只有一个固定模板。

一篇技术教程需要清晰步骤、代码块和提示框；一篇个人随笔需要留白、温度和更柔和的节奏；一篇产品发布需要亮点卡片、功能分区和更现代的视觉气质；一篇深度分析则需要更像杂志或报纸的结构感。

所以这个 Skill 默认使用：

```bash
--theme auto
```

它会先判断文章场景，再选择合适的主题和排版模块。

## 安装

手动安装：

```bash
mkdir -p ~/.codex/skills
cp -R skills/chenly-wechat-studio ~/.codex/skills/chenly-wechat-studio
```

也可以让 Codex 从 GitHub 仓库安装：

```text
Install the skill from https://github.com/LIyvqi/chenly-wechat-studio/tree/main/skills/chenly-wechat-studio
```

安装后重启 Codex，让新的 Skill 生效。

## 最常用的方式

用 Codex 调用：

```text
用 $chenly-wechat-studio 帮我把这篇 Markdown 做成公众号草稿，自动选择审美，必要时规划封面和正文图片。
```

本地渲染预览：

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/render_wechat_html.py article.md -o article.wechat.html --theme auto
```

渲染可提交到微信的正文片段：

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/render_wechat_html.py article.md -o article.submitted.html --fragment --compact --theme auto
```

生成 dry-run 草稿 payload：

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/submit_wechat_draft.py article.md --cover cover.png --theme auto
```

真实创建公众号草稿：

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/submit_wechat_draft.py article.md --cover cover.png --theme auto --submit
```

## Markdown Frontmatter

建议在文章开头写 frontmatter，让 Skill 更准确地理解文章意图：

```yaml
---
title: "文章标题"
author: "作者名"
digest: "公众号摘要，建议 120 字以内"
article_type: tutorial
visual_direction: clear-engineering
---
```

常见 `article_type`：

- `tutorial`：教程、上手指南、工具流程。
- `product`：产品发布、功能介绍、工具说明。
- `analysis`：趋势、行业、策略、深度分析。
- `news`：新闻、热点、快讯、时效性内容。
- `essay`：随笔、个人表达、创作者手记。
- `interview`：访谈、问答、对话稿。
- `case-study`：案例、复盘、项目总结。
- `listicle`：清单、合集、推荐。
- `literary`：文化、读书、文学表达。
- `opinion`：观点、评论、批判性文章。

常见 `visual_direction`：

- `clear-engineering`：清爽技术感。
- `modern-product-editorial`：现代产品感。
- `magazine-editorial`：杂志式深度文章。
- `press-newsroom`：报纸和新闻室气质。
- `warm-human-editorial`：温暖的人文叙事。
- `quiet-ink`：安静、克制、偏文学。
- `bold-opinion`：观点明确、对比更强。
- `wechat-native`：更接近微信原生阅读感。

即使不写这些字段，`--theme auto` 也会根据正文自动推断。

## 支持的排版模块

普通 Markdown：

- 标题、段落、加粗、斜体、链接、图片。
- 引用、列表、分割线、代码块。
- 简单 Markdown 表格。

增强模块：

```markdown
> [!tip] 使用建议
> 第一次先 dry-run，看预览和提交正文，再决定是否真正提交。
```

```markdown
> [!important] 核心判断
> 好看的公众号排版不是装饰更多，而是让阅读更顺。
```

```markdown
:::stat[人工操作]
更少
把重复排版、导出和草稿 payload 准备交给本地工作流。
:::
```

```markdown
:::dialogue[一次真实对话]
我：这个流程能自动提交吗？
Codex：可以，但要先配置微信开发凭证和 IP 白名单。
:::
```

```markdown
:::byline[Chenly Travel]
这是一套面向真实公众号发布的本地工作流。
:::
```

行内高亮：

```markdown
我真正想要的是 ==根据文章内容自己选择审美==。
```

## 真实提交到公众号

真实提交依赖本地 `md2wechat` CLI 调用微信公众号接口，它只负责微信 API 操作：

- 上传封面图。
- 上传本地正文图片并改写图片地址。
- 创建微信公众号草稿。

你需要在本地配置微信公众号开发凭证和 IP 白名单。不要把任何真实凭证提交到仓库。

可以使用环境变量：

```bash
export WECHAT_APPID="your_appid"
export WECHAT_SECRET="your_appsecret"
```

或者使用你自己的本地配置文件。无论哪种方式，都不要提交真实凭证、access token、草稿 payload 里的私有 media_id，或任何本地配置文件。

## 输出文件

`submit_wechat_draft.py` 会生成这些文件：

- `*.wechat.html`：本地完整预览页面。
- `*.body.html`：可读的正文 HTML。
- `*.submitted.body.html`：真实提交到微信草稿的紧凑正文。
- `*.draft.json`：最终草稿 payload。
- `*.image-uploads.json`：正文图片上传映射。

真实发布前优先检查 `*.submitted.body.html`，不要只看本地完整预览页。微信编辑器接收的是正文 HTML，不是完整网页外壳。

## 仓库结构

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
        │   ├── aesthetic-system.md
        │   ├── image-playbook.md
        │   └── style-guide.md
        └── scripts/
            ├── plan_wechat_images.py
            ├── render_wechat_html.py
            └── submit_wechat_draft.py
```

## 开源安全提醒

请不要提交：

- 微信公众号 AppID/AppSecret。
- access token。
- 私有 media_id。
- 本地 `config.yaml`。
- `.env` 文件。
- 已生成的 `*.draft.json` 和 `*.image-uploads.json`。

仓库已经配置 `.gitignore` 和 GitHub Actions 基础检查，但真正的安全习惯仍然要靠自己把关。

## License

MIT.
