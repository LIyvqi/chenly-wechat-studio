# Chenly WeChat Studio

![Chenly WeChat Studio](docs/images/hero-anime.png)

`chenly-wechat-studio` 是一个 Codex Skill：把 Markdown 做成公众号草稿。

它做三件事：

- 判断文章类型，自动选择适合的公众号审美。
- 渲染微信正文 HTML，并生成可检查的草稿 payload。
- 需要时上传封面/正文图片，并创建公众号草稿。

不需要 `MD2WECHAT_API_KEY`，也不调用 md2wechat.cn 转换接口。

## 安装

```bash
mkdir -p ~/.codex/skills
cp -R skills/chenly-wechat-studio ~/.codex/skills/chenly-wechat-studio
```

或让 Codex 从 GitHub 安装：

```text
Install the skill from https://github.com/LIyvqi/chenly-wechat-studio/tree/main/skills/chenly-wechat-studio
```

安装后重启 Codex。

## 直接使用

对 Codex 说：

```text
用 $chenly-wechat-studio 把 article.md 做成公众号草稿，自动选择审美。
```

本地预览：

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/render_wechat_html.py article.md -o article.wechat.html --theme auto
```

生成 dry-run 草稿，不提交公众号：

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/submit_wechat_draft.py article.md --cover cover.png --theme auto
```

确认没问题后提交公众号草稿：

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/submit_wechat_draft.py article.md --cover cover.png --theme auto --submit
```

## 文章格式

```markdown
---
title: "文章标题"
author: "作者"
digest: "公众号摘要"
article_type: tutorial
visual_direction: clear-engineering
---

# 文章标题

第一段会被当作开场导语。

## 一个小节

> [!tip] 提示
> 先 dry-run，再提交。
```

常用 `article_type`：

- `tutorial`：教程
- `product`：产品介绍
- `analysis`：深度分析
- `essay`：随笔
- `interview`：访谈
- `case-study`：复盘

`--theme auto` 会根据正文自动推断；写 frontmatter 会更稳。

## 输出文件

dry-run 后重点看这几个：

- `*.wechat.html`：本地预览。
- `*.submitted.body.html`：真实提交给微信的正文。
- `*.draft.json`：草稿 payload。

真实提交前确认：

- 标题和摘要没问题。
- 封面图存在。
- 正文图片已经上传并改写。
- `remaining_local_images` 为空。
- `empty_paragraph_count` 为 0。

## 公众号配置

真实提交需要本地配置微信公众号凭证和 IP 白名单。

可以用环境变量：

```bash
export WECHAT_APPID="your_appid"
export WECHAT_SECRET="your_appsecret"
```

不要提交真实 AppID/AppSecret、access token、media_id、`.env`、`config.yaml` 或 `*.draft.json`。

## 示例

看 [examples/article.md](examples/article.md)。它是一篇可以直接渲染的中文示例。

## License

MIT.
