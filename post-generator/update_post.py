#!/usr/bin/env python3
"""Update a previous post with a link to a newer post."""

import argparse
import re
from pathlib import Path


def update_content(content: str, url: str, title: str) -> str:
    """Return updated HTML content linking to the newer post."""
    updated = content.replace("{{NEWER_POST_LINK}}", url).replace("{{NEWER_POST_TITLE}}", title)

    if "{{NEWER_POST_LINK}}" in content or "{{NEWER_POST_TITLE}}" in content:
        return updated

    anchor_pattern = r'(<a class="prev-post" href=")([^"]*)("?>\s*<span class="post-nav-label">Newer)'
    if re.search(anchor_pattern, updated):
        updated = re.sub(anchor_pattern, r"\1" + url + r"\3", updated)
        title_pattern = (
            r"(<span class=\"post-nav-label\">Newer&nbsp;.*?</span><br>\s*<span>)([^<]*)(</span>)"
        )
        updated = re.sub(title_pattern, r"\1" + title + r"\3", updated, flags=re.DOTALL)
        return updated

    nav_block = re.compile(r'(<div class="post-nav thin">\n(?:.*\n)*?)(\s*</div>)', re.DOTALL)
    match = nav_block.search(updated)
    if match:
        anchor = (
            '          <a class="prev-post" href="{url}">\n'
            '            <span class="post-nav-label">Newer&nbsp;<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="feather feather-arrow-right"><line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline></svg></span><br>\n'
            '            <span>{title}</span>\n'
            '          </a>\n'
        ).format(url=url, title=title)
        updated = updated.replace(match.group(0), match.group(1) + anchor + match.group(2))
    return updated


def main() -> None:
    parser = argparse.ArgumentParser(description="Update previous post HTML with link to the new post.")
    parser.add_argument("previous_html", help="Path to previous post's HTML file")
    parser.add_argument("new_url", help="URL of the new post")
    parser.add_argument("new_title", help="Title of the new post")
    args = parser.parse_args()

    path = Path(args.previous_html)
    content = path.read_text(encoding="utf-8")
    updated = update_content(content, args.new_url, args.new_title)
    path.write_text(updated, encoding="utf-8")


if __name__ == "__main__":
    main()
