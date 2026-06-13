---
title: "Draft Post - Local Preview Only"
date: 2026-06-13
description: "This is a draft post. It should compile locally, but should be excluded from production deployments."
tags: [testing, drafts]
dev: true
ai_usage: no-ai
---

This is a draft post used to test our compiler's **Production Build Mode**.

If you are running `build.py` locally (which runs in **Development Mode** by default), you will be able to see this post card on the homepage and click to read this content.

However, if you run the build with the `--prod` flag or when it builds automatically via GitHub Actions (which run in **Production Mode**), this post will be completely ignored:
- No `posts/test-draft.html` file will be generated.
- No card for this post will show up on the homepage.
- No reference to this post will be included in `sitemap.xml`.

This lets you write and preview drafts locally without exposing them to search engines or public visitors.
