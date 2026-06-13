---
title: "Building a Lightweight Static Site Builder"
date: 2026-06-13
description: "How I created a zero-dependency dev blog with a custom Python build script, Solarized Light theme, and uv."
tags: [python, webdev, setup]
---

Welcome to my development blog! In this article, I want to share the design and code behind the static site generator that compiles the very page you are reading.

When setting up a development blog, many developers default to Jekyll or Hugo. While those are excellent tools, they can sometimes bring complex dependency trees. Since I wanted a **zero-dependency, lightweight setup** that works instantly on Windows, macOS, and Linux, I decided to build a simple compiler in Python.

## Why Python and `uv`?

`uv` is an extremely fast package manager written in Rust. It lets us run scripts with inline dependency metadata, meaning we don't even need to pre-install `markdown` or `pyyaml` globally. We just run:

```bash
uv run build.py
```

Here's the core front-matter parser and directory builder from our `build.py`:

```python
import os
import yaml
import markdown

def parse_post(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract YAML front matter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            metadata = yaml.safe_load(parts[1]) or {}
            markdown_body = parts[2]
            return metadata, markdown_body
            
    return {}, content
```

## Designing the Solarized Light Aesthetic

Solarized is a highly refined color palette created by Ethan Schoonover. It reduces contrast while preserving readability, making it extremely easy on the eyes during long development sessions. 

The color variables are defined in our CSS:

```css
:root {
  --base3: #fdf6e3;  /* Page background */
  --base2: #eee8d5;  /* Secondary background */
  --base00: #657b83; /* Primary body text */
  --base01: #586e75; /* Headings */
  --blue: #268bd2;   /* Main link / primary accent */
  --cyan: #2aa198;   /* Secondary accent */
}
```

### Table Comparison of Static Engines

Here is a quick comparison of why a custom script fits this setup:

| Feature | Hugo | Jekyll | Custom Python (`uv`) |
| :--- | :--- | :--- | :--- |
| **Install size** | ~50MB | ~100MB+ (Ruby) | **0MB (ephemeral via uv)** |
| **Build speed** | Blazing | Slow | Blazing |
| **Customizability** | Medium (Go templates) | Medium (Liquid) | **Unlimited (Python + Plain HTML)** |
| **Learning Curve** | High | Medium | **None (Basic Python)** |

## Bulleted Walkthrough

Here is what the compiler does behind the scenes:

- **Scans** `content/posts/` for any markdown (`.md`) files.
- **Extracts** front matter metadata like title, date, and tags.
- **Converts** the markdown body into standard HTML elements.
- **Renders** code syntax highlighting dynamically using Prism.js loaded from CDN.
- **Injects** the content into a standard template (`layout.html`).
- **Generates** an interactive `index.html` listing all posts, featuring client-side tag filtering.

> "Simplicity is the ultimate sophistication." 
> — Leonardo da Vinci (and the core guideline for this site)

If you'd like to use this setup yourself, feel free to clone my repository and start writing markdown files!
