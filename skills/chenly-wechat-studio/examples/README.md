# Chenly WeChat Studio Examples

These examples are meant to be copied into Codex. They show that the skill is not limited to Markdown conversion: you can start with an idea, a messy brief, a few notes, or a full Markdown draft.

## 1. Start From A Loose Idea

```text
Use $chenly-wechat-studio.

我想写一篇公众号文章，主题是“我为什么开始用 AI 处理公众号排版”。
我还没有 Markdown，只有几个想法：

- 以前每次排版都很耗时间。
- 我希望文章不是模板感，而是根据内容自动变漂亮。
- 这套流程应该适合个人创作者和小团队。
- 最后想引导读者试试“先说内容，再让 Codex 实现文章”的方式。

请你帮我完成：
1. 文章标题、摘要和结构
2. 正文初稿
3. 适合公众号的排版模块
4. 封面方向
5. 本地预览 HTML
```

## 2. Turn Spoken Content Into A Polished Article

```text
Use $chenly-wechat-studio.

下面是我随口说的内容，请你整理成一篇公众号文章，不要只是照着转写。
读者是做内容运营的人，语气要自然、有经验感，不要太像 AI。

内容：
我最近发现公众号排版最麻烦的地方不是把文字变好看，而是不知道每篇文章适合什么样的结构。有些是教程，有些是复盘，有些是观点，如果都套同一个模板，就会很僵硬。所以我做了一个 skill，让 Codex 先判断文章类型，再选择视觉方向，然后再生成公众号可用的 HTML。它可以从一句话开始，也可以从 Markdown 开始。

请你补足文章逻辑，并输出可渲染的 Markdown 和预览 HTML。
```

## 3. Improve An Existing Markdown Draft

```text
Use $chenly-wechat-studio.

请读取 `article.md`，不要直接覆盖原文。
帮我做一次公众号发布前优化：

- 判断文章类型和读者
- 改善开头钩子
- 拆分过长段落
- 增加必要的标题、引用或提示模块
- 自动选择主题
- 输出 `article.wechat.md` 和 `article.wechat.html`

这篇文章希望看起来更高级，但不要堆装饰。
```

## 4. Plan Cover And Body Images

```text
Use $chenly-wechat-studio.

我准备发一篇旅行攻略，主题是“曼谷第一次自由行怎么安排”。
我希望图片真实、美观，不要全是 AI 感。

请你先做 image plan：
- 哪些地方应该用真实图片或地图参考
- 哪些地方可以生成概念图
- 封面图 prompt
- 正文配图位置
- 图片文件名建议

然后再帮我把文章排成公众号风格。
```

## 5. Prepare A Draft Without Submitting

```text
Use $chenly-wechat-studio.

请把 `article.md` 和 `cover.png` 准备成公众号草稿 payload，但不要提交到微信。
请输出：

- 本地预览 HTML
- body HTML
- compact submitted body HTML
- draft JSON
- 主题和文章类型
- 是否还有本地图片未上传
- 标题、摘要是否超长
```

## 6. Full Content Collaboration

```text
Use $chenly-wechat-studio.

我只给你方向，你来完成文章实现：

主题：为什么“会表达需求”会成为 AI 时代的内容生产能力
读者：公众号作者、独立开发者、内容运营
目标：让读者理解，不必先写好完整文章，也可以通过和 Codex 协作完成高质量成稿
语气：清醒、温和、有一点鼓励
视觉：高级但克制，像一篇认真打磨过的编辑部文章

请你完成文章、排版、封面方向、图片计划和本地预览。
```
