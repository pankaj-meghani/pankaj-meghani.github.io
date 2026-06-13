# Solarized Light Developer Blog

A lightweight, premium, zero-dependency development blog designed with a modern **Solarized Light theme**. 

This blog runs completely dependency-free without requiring complex setups like Ruby (Jekyll) or Node.js (Astro). It uses **`uv`** to run a simple, fast Python-based compiler that converts Markdown posts into SEO-friendly, semantic static HTML.

## 📁 Directory Structure

```text
adventurous-mendeleev/
├── .github/workflows/
│   └── deploy.yml       # GitHub Actions automated deploy script
├── content/posts/
│   └── hello-world.md   # Write your markdown posts here!
├── src/
│   ├── index-template.html # Homepage layout template
│   ├── layout.html         # Individual article layout template
│   └── styles.css          # Solarized Light stylesheet
├── posts/               # [Auto-Generated] Compiled blog posts
├── index.html           # [Auto-Generated] Compiled homepage
├── styles.css           # [Auto-Generated] Main stylesheet copy
└── build.py             # Custom compiler script (run via uv)
```

---

## 🚀 Getting Started

Ensure you have [uv](https://github.com/astral-sh/uv) installed on your system.

### 1. Build the Blog
To compile your Markdown posts into HTML, run:
```bash
uv run build.py
```
This script will automatically download Python and the required parsing libraries (`markdown` and `pyyaml`) in a fast, isolated cache, then compile all your posts.

### 2. Preview Locally
Start a local static server to preview the site:
```bash
uv run python -m http.server 8080
```
Open [http://localhost:8080](http://localhost:8080) in your web browser.

---

## ✍️ How to Write a Post

To write a new blog post, simply create a new Markdown file inside `content/posts/` (e.g., `content/posts/my-new-post.md`).

Every post must start with a **YAML front matter** section enclosed in `---` dashes. Here is a starter template:

```markdown
---
title: "My New Developer Article"
date: 2026-06-13
description: "A short, engaging summary of what this blog post is about."
tags: [javascript, webdev, tutorial]
---

Write your article in standard Markdown here.

### Writing Code
You can write code blocks using triple backticks and the language specifier:

```javascript
const greet = (name) => `Hello, ${name}!`;
console.log(greet("World"));
```

Prism.js will automatically detect the language and apply a beautiful Solarized syntax highlighting style with a copy-to-clipboard button.
```

After saving your file, run `uv run build.py` to compile it!

---

## 🌐 Deploying to GitHub Pages

This repository is pre-configured with a GitHub Actions workflow to publish your blog automatically.

1. **Enable GitHub Pages** in your repository settings:
   - Go to your repository on GitHub.
   - Click on **Settings** -> **Pages** (under Code and automation).
   - Under **Build and deployment**, set **Source** to **GitHub Actions**.
2. **Push to GitHub**:
   - Push your code to your repository's `main` or `master` branch.
   - The workflow will automatically trigger, build the website, and deploy it to your GitHub Pages URL (e.g., `https://<your-username>.github.io/<your-repo-name>/`).
