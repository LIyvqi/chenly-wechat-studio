---
title: "我用 Codex 做了一个公众号生产工坊"
author: "Chenly Travel"
digest: "这是一套从 Markdown 到公众号草稿的本地工作流：AI 负责审美、结构和图片规划，脚本负责渲染、检查和提交。"
article_type: tutorial
visual_direction: clear-engineering
---

# 我用 Codex 做了一个公众号生产工坊

我一直想要的不是一个固定模板，而是一套能根据文章内容自己选择排版气质的公众号生产流程。

如果是一篇技术教程，它应该清爽、稳定、步骤明确；如果是一篇产品介绍，它应该更像一篇克制的发布稿；如果是一篇随笔，它应该有留白、有温度、有节奏。公众号文章真正需要的不是“装饰更多”，而是 ==让内容以合适的样子出现==。

## 这个 Skill 是什么

`chenly-wechat-studio` 是一个面向 Codex 的公众号文章生产 Skill。

它把公众号发文流程拆成几件事：

- Codex 负责理解文章、调整结构、判断审美方向。
- 本地脚本负责把 Markdown 渲染成公众号正文优先的 HTML。
- 图片流程负责规划封面和正文视觉。
- 提交流程负责 dry-run、上传图片、生成草稿 payload，必要时创建微信公众号草稿。

> [!important] 核心判断
> 这个 Skill 不是“固定排版模板”，而是一个会根据内容场景选择视觉语言的公众号工作流。

## 为什么不做成固定模板

公众号文章的场景差异很大。

一篇文章可能是：

1. 教程：读者要照着一步步做。
2. 产品发布：读者要快速理解亮点。
3. 深度分析：读者需要信任感和结构感。
4. 随笔：读者需要更自然的阅读节奏。
5. 访谈：读者需要清楚地区分人物和对话。

如果所有内容都套一个模板，短期看起来统一，长期就会显得僵硬。这个 Skill 更适合做成“编辑判断层 + 渲染执行层”。

:::stat[默认策略]
--theme auto
先判断内容，再决定审美，而不是让用户每次手动选模板。
:::

## 它的典型工作流

最常见的流程是：

- 准备一篇 Markdown 文章。
- 在 frontmatter 里写标题、作者、摘要和文章类型。
- 让 Codex 根据内容判断视觉方向。
- 先 dry-run，生成本地预览和草稿 JSON。
- 检查正文 HTML、封面、图片和摘要。
- 确认无误后再提交到公众号草稿箱。

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/submit_wechat_draft.py article.md --cover cover.png --theme auto
```

真实提交时再加：

```bash
python3 ~/.codex/skills/chenly-wechat-studio/scripts/submit_wechat_draft.py article.md --cover cover.png --theme auto --submit
```

> [!tip] 建议
> 第一次使用时先不要加 `--submit`。先看 `*.wechat.html`、`*.body.html`、`*.submitted.body.html` 和 `*.draft.json`，确认没问题再创建真实草稿。

## frontmatter 怎么写

建议每篇文章开头都写一段 frontmatter：

```yaml
---
title: "我用 Codex 做了一个公众号生产工坊"
author: "Chenly Travel"
digest: "这是一套从 Markdown 到公众号草稿的本地工作流。"
article_type: tutorial
visual_direction: clear-engineering
---
```

其中：

- `title` 是公众号标题。
- `author` 是作者名。
- `digest` 是公众号摘要。
- `article_type` 帮助 Skill 判断文章场景。
- `visual_direction` 帮助 Skill 判断视觉气质。

即使不写 `article_type` 和 `visual_direction`，`--theme auto` 也会从正文里推断。但写清楚会更稳。

## 支持哪些文章场景

这个 Skill 内置了多个常见场景：

| 场景 | 适合内容 | 视觉方向 |
| --- | --- | --- |
| `tutorial` | 教程、安装、工具流程 | 清爽技术感 |
| `product` | 产品发布、功能介绍 | 现代产品感 |
| `analysis` | 深度分析、趋势判断 | 杂志式结构 |
| `news` | 热点、快讯、更新 | 新闻室气质 |
| `essay` | 随笔、个人表达 | 温暖叙事 |
| `interview` | 访谈、问答、对话 | 杂志访谈感 |
| `case-study` | 案例、复盘、项目总结 | 报告感 |
| `listicle` | 清单、合集、推荐 | 卡片式扫描 |
| `literary` | 文化、读书、文学 | 安静克制 |
| `opinion` | 观点、评论、批判 | 对比更强 |

## 增强排版模块

除了普通 Markdown，这个 Skill 还支持一些更适合公众号的模块。

比如提示块：

> [!warning] 注意
> 如果正文里引用了本地图片，真实提交前需要上传并改写成微信可访问的图片地址。封面上传不等于正文图片上传。

比如对话块：

:::dialogue[一次真实对话]
我：这个流程能自动提交吗？
Codex：可以，但要先配置微信开发凭证和 IP 白名单。
我：那我人工操作能少一点吗？
Codex：可以。先 dry-run 检查，再一键提交草稿。
:::

比如作者手记：

:::byline[Chenly Travel]
我更希望它像一个长期可迭代的公众号工坊，而不是一次性的 Markdown 转换脚本。
:::

## 开源时要注意什么

这个项目可以开源，但真实公众号配置不能进仓库。

不要提交：

- 微信公众号开发凭证。
- access token。
- 私有 media_id。
- 本地配置文件。
- 真实草稿 payload。

这也是为什么这个仓库只放 Skill、脚本、参考说明和示例文章；真实发布所需的账号配置应该留在每个人自己的本地环境里。

## 总结

`chenly-wechat-studio` 的目标很简单：

让公众号文章从“写完一篇 Markdown”到“生成一个能看的公众号草稿”，中间少一点重复劳动，多一点审美判断。

它不替代作者的判断，但可以把那些机械、琐碎、容易出错的步骤接过去。

最后，人负责表达，Codex 负责把表达打磨成适合公众号阅读的样子。
