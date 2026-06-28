# Local WeChat Article Style Guide

Use this reference when rewriting or heavily formatting a WeChat Official Account article with Codex.

## Reading Shape

- Optimize for mobile scanning.
- Prefer paragraphs of 1-3 sentences.
- Use `##` headings to create clear pauses.
- Avoid more than two heading levels unless the article is a tutorial.
- Keep lists short; if a list needs more than seven items, group it.
- Treat the opening paragraph as the article's lead: it should state the promise, tension, or useful payoff.
- Use one strong idea per section; if a section has multiple claims, split it.
- Mix paragraph lengths intentionally. All-long paragraphs feel oppressive; all-short paragraphs make the article feel broken.

## Voice

- Keep claims concrete and grounded.
- Remove generic AI filler such as "in today's fast-paced world", "it is worth noting", and repetitive "not only...but also" constructions.
- Do not add statistics, quotes, case studies, or product claims unless present in the source or supplied by the user.
- Preserve the user's actual viewpoint even when polishing the prose.

## WeChat HTML Constraints

- Prefer inline styles over stylesheet dependencies.
- Avoid script tags and interactive behavior.
- Avoid external fonts.
- Avoid complex CSS layout that may be stripped by the WeChat editor.
- Use images conservatively; local images still need a publishing/upload step.

## Aesthetic Direction

- Build a first-screen rhythm: title, small metadata, digest, lead block, then the first useful section.
- Make visual blocks earn their place. Use lead cards, quote blocks, list cards, and code panels to clarify structure, not to decorate every paragraph.
- Prefer editorial calm over poster-like noise. One accent color and one soft surface color are usually enough.
- Keep the final HTML usable even if the WeChat editor strips a few advanced CSS properties.
- For cover images, avoid in-image text. Let the article title carry the words.
- If the article's business scene matters, read `aesthetic-system.md` and choose `--theme auto` or a scenario-specific theme.
- If images matter, read `image-playbook.md` and choose whether each image should be real/sourced, user-provided, generated, or omitted.

## Module Use

- Use `> [!important]` for a core judgment, not for ordinary emphasis.
- Use `> [!tip]` for practical advice in tutorials and tool articles.
- Use `> [!warning]` only for a real limitation, risk, or publishing caveat.
- Use `:::stat[Label]` when one number deserves visual weight.
- Use `:::dialogue[Title]` only for real dialogue or interview turns.
- Use `==highlight==` sparingly; too many highlights make the article feel noisy.

## Image Rhythm

- The first visual should arrive early enough to help the first screen.
- Real screenshots/photos are better than generated images when the article claims a real place, product, interface, or result.
- Generated images are best for cover visuals, concepts, process explainers, friendly diagrams, and anonymized UI mockups.
- Every body image should have a short caption or surrounding sentence that explains why it is there.
- Avoid image runs where three images in a row have the same shape and no new job.

## Light Review

Before submitting to WeChat draft:

- Title is 32 characters or fewer.
- Digest is 128 characters or fewer and makes sense outside the article.
- Opening lead is not generic.
- Theme fits the article type.
- Cover exists and has no readable fake text or watermark.
- Image plan/source notes exist when the article uses generated or sourced visuals.
- Body images are meaningful, readable on mobile, and not just decoration.
- Draft JSON has `title`, `digest`, `content`, and a cover media id when submitting.

## Deliverables

For a local conversion task, produce:

1. A rendered `.wechat.html` file for preview/copy.
2. Optionally, a `.wechat.md` polished Markdown file if the user asked for rewriting or wants an editable source.
3. A short summary of theme, output path, and any image/publishing caveats.
