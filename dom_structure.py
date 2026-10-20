"""DOM Structural Skeletonization, Aggregation, Synthetic Generation, and Archive Ingestion.

Focuses purely on HTML DOM topology and element hierarchy (from <html> to </html>)
without retaining body text, Avoiding text copyright/rights concerns.
"""
from __future__ import annotations

import hashlib
import json
import random
import re
from collections import Counter
from html.parser import HTMLParser

try:
    from selectolax.lexbor import LexborHTMLParser as LexborParser
except ImportError:
    from selectolax.parser import HTMLParser as LexborParser

SCHEMA = "blueprobe-dom-structure/1"

_VOID_TAGS = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
_STRIP_TAGS = {"script", "style", "template", "noscript", "svg"}

COMMON_CONTAINER_TAGS = ["div", "section", "article", "main", "aside", "header", "footer", "nav"]
COMMON_LIST_TAGS = ["ul", "ol", "li"]
COMMON_TEXT_CONTAINER_TAGS = ["p", "h1", "h2", "h3", "span", "blockquote"]
COMMON_INTERACTIVE_TAGS = ["a", "button", "input", "select", "form"]
COMMON_TABLE_TAGS = ["table", "tr", "td", "th", "tbody", "thead"]


class _SkeletonParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.output: list[str] = []
        self.skip_stack: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        tag_lower = tag.lower()
        if self.skip_stack or tag_lower in _STRIP_TAGS:
            self.skip_stack.append(tag_lower)
            return

        attr_str = ""
        filtered_attrs = []
        for k, v in attrs:
            if v is not None:
                # Strip text values from aria-label / title / placeholder to keep structural metadata clean
                val = v if k.lower() in ("id", "class", "role", "type", "name", "for", "itemprop", "itemtype") else ""
                filtered_attrs.append(f'{k}="{val}"' if val else k)
            else:
                filtered_attrs.append(k)

        if filtered_attrs:
            attr_str = " " + " ".join(filtered_attrs)

        if tag_lower in _VOID_TAGS:
            self.output.append(f"<{tag_lower}{attr_str} />")
        else:
            self.output.append(f"<{tag_lower}{attr_str}>")

    def handle_endtag(self, tag: str):
        tag_lower = tag.lower()
        if self.skip_stack:
            if self.skip_stack[-1] == tag_lower:
                self.skip_stack.pop()
            return

        if tag_lower not in _VOID_TAGS:
            self.output.append(f"</{tag_lower}>")

    def handle_data(self, data: str):
        # Ignore all text data to strip text content
        pass


def skeletonize(html: str) -> str:
    """Strip all text content and return pure HTML DOM structural skeleton.

    Retains element tag hierarchy, nesting, and structural attributes (id, class, role, etc.).
    """
    if not isinstance(html, str) or not html.strip():
        return "<html><head></head><body></body></html>"

    parser = _SkeletonParser()
    try:
        parser.feed(html)
        parser.close()
        skeleton = "".join(parser.output)
    except Exception:
        # Fallback regex strip if HTML is severely malformed
        skeleton = re.sub(r">[^<]+<", "><", html)
        skeleton = re.sub(r"<(script|style|svg)[^>]*>.*?</\1>", "", skeleton, flags=re.DOTALL | re.IGNORECASE)

    if not skeleton.startswith("<html"):
        skeleton = f"<html><body>{skeleton}</body></html>"

    return skeleton


def structural_fingerprint(html: str) -> dict:
    """Compute structural metrics and fingerprint for a given HTML DOM tree."""
    skeleton = skeletonize(html)
    tree = LexborParser(skeleton)

    tag_counts: Counter[str] = Counter()
    max_depth = 0

    def _walk(node, depth):
        nonlocal max_depth
        if depth > max_depth:
            max_depth = depth
        if node.tag and node.tag != "-root":
            tag_counts[node.tag.lower()] += 1
        child = node.child
        while child is not None:
            _walk(child, depth + 1)
            child = child.next

    if tree.root:
        _walk(tree.root, 0)

    skeleton_hash = hashlib.sha256(skeleton.encode("utf-8")).hexdigest()

    # Concise structural signature: top 5 tags and depth
    top_tags = ",".join(f"{tag}:{count}" for tag, count in tag_counts.most_common(5))
    path_sig = f"d{max_depth}_n{sum(tag_counts.values())}[{top_tags}]"

    return {
        "schema": "blueprobe-dom-fingerprint/1",
        "max_depth": max_depth,
        "total_nodes": sum(tag_counts.values()),
        "tag_counts": dict(tag_counts),
        "skeleton_sha256": skeleton_hash,
        "structural_signature": path_sig,
    }


def generate_random_dom(depth: int = 3, max_breadth: int = 3, seed: int | None = None) -> str:
    """Generate a synthetic random HTML DOM skeleton for testing topology variations."""
    if seed is not None:
        rng = random.Random(seed)
    else:
        rng = random.Random()

    classes = ["container", "wrapper", "card", "content", "sidebar", "nav-item", "btn", "header", "footer"]
    roles = ["main", "navigation", "banner", "contentinfo", "article", "region"]

    def _build_element(current_depth: int) -> str:
        if current_depth >= depth:
            leaf_tag = rng.choice(COMMON_TEXT_CONTAINER_TAGS + COMMON_INTERACTIVE_TAGS)
            cls = rng.choice(classes) if rng.random() > 0.5 else ""
            cls_attr = f' class="{cls}"' if cls else ""
            if leaf_tag in _VOID_TAGS:
                return f"<{leaf_tag}{cls_attr} />"
            return f"<{leaf_tag}{cls_attr}></{leaf_tag}>"

        tag = rng.choice(COMMON_CONTAINER_TAGS)
        attr_parts = []
        if rng.random() > 0.4:
            attr_parts.append(f'class="{rng.choice(classes)}"')
        if rng.random() > 0.6:
            attr_parts.append(f'role="{rng.choice(roles)}"')

        attr_str = " " + " ".join(attr_parts) if attr_parts else ""
        num_children = rng.randint(1, max(1, max_breadth))
        children_html = "".join(_build_element(current_depth + 1) for _ in range(num_children))
        return f"<{tag}{attr_str}>{children_html}</{tag}>"

    body_children = "".join(_build_element(1) for _ in range(rng.randint(1, max_breadth)))
    return f"<!DOCTYPE html><html><head><meta charset=\"utf-8\" /><title></title></head><body>{body_children}</body></html>"


def ingest_har(har_data: str | dict | bytes) -> list[dict]:
    """Ingest HAR (HTTP Archive) JSON and extract DOM structural skeletons for all HTML entries."""
    if isinstance(har_data, bytes):
        har_data = har_data.decode("utf-8")
    if isinstance(har_data, str):
        har_data = json.loads(har_data)

    entries = har_data.get("log", {}).get("entries", [])
    results = []

    for index, entry in enumerate(entries):
        request = entry.get("request", {})
        response = entry.get("response", {})
        url = request.get("url", "")
        status = response.get("status", 0)
        content = response.get("content", {})
        mime = content.get("mimeType", "").lower()
        text = content.get("text", "")

        if ("html" in mime or url.endswith((".html", ".htm"))) and text:
            skeleton = skeletonize(text)
            fingerprint = structural_fingerprint(text)
            results.append({
                "entry_index": index,
                "url": url,
                "status": status,
                "mime_type": mime,
                "skeleton": skeleton,
                "fingerprint": fingerprint,
            })

    return results
