# /// script
# dependencies = [
#   "markdown",
#   "pyyaml",
# ]
# ///

import os
import re
import yaml
import markdown
import shutil
from datetime import datetime

def format_date(date_val):
    if isinstance(date_val, datetime):
        return date_val.strftime("%B %d, %Y"), date_val.strftime("%Y-%m-%d")
    elif hasattr(date_val, "strftime"):  # datetime.date
        return date_val.strftime("%B %d, %Y"), date_val.strftime("%Y-%m-%d")
    
    # Fallback if it's a string
    try:
        dt = datetime.strptime(str(date_val).strip(), "%Y-%m-%d")
        return dt.strftime("%B %d, %Y"), dt.strftime("%Y-%m-%d")
    except ValueError:
        return str(date_val), str(date_val)

def main():
    print("[Build] Starting Solarized Light Blog Compiler...")
    
    # Paths
    content_dir = os.path.join("content", "posts")
    output_posts_dir = "posts"
    src_dir = "src"
    
    # Ensure directories exist
    os.makedirs(content_dir, exist_ok=True)
    os.makedirs(output_posts_dir, exist_ok=True)
    
    # Copy stylesheet to root
    shutil.copy2(os.path.join(src_dir, "styles.css"), "styles.css")
    print("[OK] Copied stylesheet to root directory")
    
    # Load templates
    with open(os.path.join(src_dir, "layout.html"), "r", encoding="utf-8") as f:
        layout_template = f.read()
    with open(os.path.join(src_dir, "index-template.html"), "r", encoding="utf-8") as f:
        index_template = f.read()
        
    posts_data = []
    all_tags = set()
    
    post_files = [f for f in os.listdir(content_dir) if f.endswith(".md")]
    
    if not post_files:
        print("[WARN] No posts found in content/posts/.")
        # A default post will be created separately or we handle it gracefully here
    
    for filename in post_files:
        file_path = os.path.join(content_dir, filename)
        slug = os.path.splitext(filename)[0]
        
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()
            
        # Parse Front Matter
        metadata = {}
        markdown_body = file_content
        
        if file_content.startswith("---"):
            parts = file_content.split("---", 2)
            if len(parts) >= 3:
                try:
                    metadata = yaml.safe_load(parts[1]) or {}
                    markdown_body = parts[2]
                except Exception as e:
                    print(f"[ERR] Error parsing front matter in {filename}: {e}")
                    
        # Extract metadata fields with defaults
        title = metadata.get("title", slug.replace("-", " ").title())
        date_val = metadata.get("date", datetime.now())
        description = metadata.get("description", "A technical blog post sharing development insights.")
        tags = metadata.get("tags", [])
        if not isinstance(tags, list):
            tags = [tags]
            
        tags = [str(t).strip().lower() for t in tags if t]
        for tag in tags:
            all_tags.add(tag)
            
        formatted_date, iso_date = format_date(date_val)
        
        # Calculate reading time (~200 words per minute)
        word_count = len(re.findall(r"\w+", markdown_body))
        reading_time = max(1, round(word_count / 200))
        
        # Convert Markdown to HTML
        # Use fenced_code for block code, tables for markdown tables
        html_content = markdown.markdown(
            markdown_body, 
            extensions=["fenced_code", "tables"]
        )
        
        # Render tag badges for the article page
        tags_badges = "".join(f'<span class="post-tag">#{t}</span>' for t in tags)
        
        # Substitute into post layout
        post_html = layout_template
        replacements = {
            "{{title}}": title,
            "{{description}}": description,
            "{{date}}": iso_date,
            "{{formatted_date}}": formatted_date,
            "{{reading_time}}": str(reading_time),
            "{{tags}}": tags_badges,
            "{{content}}": html_content
        }
        for placeholder, value in replacements.items():
            post_html = post_html.replace(placeholder, value)
            
        # Save output post
        output_filename = f"{slug}.html"
        output_path = os.path.join(output_posts_dir, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(post_html)
            
        print(f"[OK] Compiled: {filename} -> {output_path}")
        
        # Keep track for the homepage index
        posts_data.append({
            "title": title,
            "slug": slug,
            "iso_date": iso_date,
            "formatted_date": formatted_date,
            "reading_time": reading_time,
            "description": description,
            "tags": tags,
            "date_obj": date_val if isinstance(date_val, datetime) else datetime.combine(date_val, datetime.min.time()) if hasattr(date_val, "strftime") else datetime.now()
        })
        
    # Sort posts chronologically (newest first)
    posts_data.sort(key=lambda x: x["date_obj"], reverse=True)
    
    # Generate posts listing HTML for index page
    posts_cards_html = []
    for post in posts_data:
        tags_str = ",".join(post["tags"])
        tags_badges = "".join(f'<span class="post-tag">#{t}</span>' for t in post["tags"])
        
        card = f"""        <article class="post-card" data-tags="{tags_str}" onclick="window.location.href='posts/{post['slug']}.html'">
          <div class="post-card-meta">
            <time datetime="{post['iso_date']}">
              <svg style="width: 14px; height: 14px; fill: currentColor; vertical-align: middle; margin-right: 3px;" viewBox="0 0 24 24">
                <path d="M19 19H5V8h14m-3-7v2H8V1H6v2H5c-1.11 0-2 .89-2 2v14a2 2 0 002 2h14a2 2 0 002-2V5a2 2 0 00-2-2h-1V1m-1 11h-5v5h5v-5z"/>
              </svg>
              {post['formatted_date']}
            </time>
            <span>•</span>
            <span>
              <svg style="width: 14px; height: 14px; fill: currentColor; vertical-align: middle; margin-right: 3px;" viewBox="0 0 24 24">
                <path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10 10-4.5 10-10S17.5 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67V7z"/>
              </svg>
              {post['reading_time']} min read
            </span>
          </div>
          <h3 class="post-card-title"><a href="posts/{post['slug']}.html">{post['title']}</a></h3>
          <p class="post-card-desc">{post['description']}</p>
          <div class="post-card-tags">
            {tags_badges}
          </div>
        </article>"""
        posts_cards_html.append(card)
        
    posts_content = "\n".join(posts_cards_html) if posts_cards_html else '        <p style="text-align: center; color: var(--text-secondary); margin: 3rem 0;">No development posts available yet. Write your first markdown post in content/posts!</p>'
    
    # Generate tag filtering buttons HTML
    tag_buttons_html = []
    for tag in sorted(all_tags):
        btn = f'<button class="tag-btn" data-tag="{tag}">#{tag}</button>'
        tag_buttons_html.append(btn)
        
    tag_buttons_content = "\n        ".join(tag_buttons_html)
    
    # Substitute into index template
    index_html = index_template
    index_html = index_html.replace("{{tag_buttons}}", tag_buttons_content)
    index_html = index_html.replace("{{posts}}", posts_content)
    
    # Save output index.html
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print("[OK] Generated index.html")
    
    # Generate Sitemap and robots.txt for SEO indexing
    site_url = "https://pankaj-meghani.github.io/personal-website/"
    today_str = datetime.now().strftime("%Y-%m-%d")
    
    sitemap_urls = [
        f"  <url>\n    <loc>{site_url}</loc>\n    <lastmod>{today_str}</lastmod>\n    <changefreq>daily</changefreq>\n    <priority>1.0</priority>\n  </url>"
    ]
    
    for post in posts_data:
        sitemap_urls.append(
            f"  <url>\n    <loc>{site_url}posts/{post['slug']}.html</loc>\n    <lastmod>{post['iso_date']}</lastmod>\n    <changefreq>weekly</changefreq>\n    <priority>0.8</priority>\n  </url>"
        )
        
    sitemap_xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(sitemap_urls) + '\n</urlset>'
    
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_xml)
    print("[OK] Generated sitemap.xml")
    
    robots_txt = f"User-agent: *\nAllow: /\n\nSitemap: {site_url}sitemap.xml\n"
    with open("robots.txt", "w", encoding="utf-8") as f:
        f.write(robots_txt)
    print("[OK] Generated robots.txt")
    
    print("[OK] Compilation complete! Run local server to view the results.")

if __name__ == "__main__":
    main()
