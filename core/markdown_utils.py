from django.utils.html import escape
from django.utils.safestring import mark_safe

import bleach
import markdown

ALLOWED_TAGS = [
    "a",
    "abbr",
    "blockquote",
    "br",
    "code",
    "dd",
    "del",
    "div",
    "dl",
    "dt",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "img",
    "li",
    "ol",
    "p",
    "pre",
    "span",
    "strong",
    "table",
    "tbody",
    "td",
    "th",
    "thead",
    "tr",
    "ul",
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title"],
    "img": ["alt", "src", "title"],
    "th": ["align"],
    "td": ["align"],
}

ALLOWED_PROTOCOLS = ["http", "https", "mailto"]


def render_markdown_safe(source):
    """Render Markdown while escaping raw HTML and sanitizing generated output."""
    if not source:
        return ""

    escaped_source = escape(source)
    rendered = markdown.markdown(
        escaped_source,
        extensions=["extra", "sane_lists"],
        output_format="html5",
    )
    cleaned = bleach.clean(
        rendered,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )
    return mark_safe(cleaned)

