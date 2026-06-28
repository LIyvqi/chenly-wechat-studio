---
title: "我用 Codex 做了一个公众号生产工坊"
author: "Chenly Travel"
digest: "从 Markdown 到公众号草稿，AI 负责审美和结构，本地脚本负责生成与提交。"
article_type: tutorial
visual_direction: clear-engineering
---

# 我用 Codex 做了一个公众号生产工坊

我想要的不是一个固定模板，而是一套能根据内容自己选择排版气质的公众号生产流程。

## 它解决什么问题

- Markdown 可以直接变成公众号正文
- 文章会根据业务场景选择视觉方向
- 封面和正文图片可以先规划再生成
- 草稿提交前会检查正文 HTML

> [!tip] 建议
> 第一次使用时先 dry-run，看 `*.wechat.html` 和 `*.submitted.body.html`，确认没问题再提交。

## 最短路径

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/submit_wechat_draft.py article.md --cover cover.png --theme auto
```

:::stat[人工操作]
更少
把重复的排版、导出、草稿 payload 准备交给本地工作流。
:::

## 我的使用原则

好看的公众号文章不应该靠堆装饰，而应该让每个视觉块都服务阅读。

:::byline[Chenly Travel]
这是一个面向真实公众号发布的 Codex skill，适合继续按自己的品牌气质迭代。
:::
