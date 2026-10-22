import json
import dom_patterns
import dom_structure


def test_skeletonize_void_tags_in_stripped_element():
    # Void tag (<img>) inside <noscript> should not corrupt skip_stack and swallow subsequent <main>
    raw_html = """
    <html>
      <head>
        <noscript><img src="tracking.gif"><p>No JS</p></noscript>
      </head>
      <body>
        <main id="valid-main"><p>Text</p></main>
      </body>
    </html>
    """
    skeleton = dom_structure.skeletonize(raw_html)
    assert '<main id="valid-main">' in skeleton
    assert "<p></p>" in skeleton


def test_skeletonize_strips_text_and_scripts():
    raw_html = """
    <!DOCTYPE html>
    <html>
      <head>
        <title>Secret Title Text</title>
        <script>console.log("sensitive js code");</script>
        <style>body { color: red; }</style>
      </head>
      <body>
        <main class="markdown-body" id="content">
          <h1>Main Article Headline</h1>
          <p>Secret user paragraph body text that must be removed for copyright safety.</p>
          <a href="https://example.com" aria-label="secret label">Click Here</a>
        </main>
      </body>
    </html>
    """
    skeleton = dom_structure.skeletonize(raw_html)
    assert "Secret Title Text" not in skeleton
    assert "sensitive js code" not in skeleton
    assert "Secret user paragraph" not in skeleton
    assert "Click Here" not in skeleton
    # Structural hierarchy and structural attributes must be preserved
    assert '<main class="markdown-body" id="content">' in skeleton
    assert "<h1>" in skeleton
    assert "</h1>" in skeleton
    assert "<a>" in skeleton or "<a" in skeleton


def test_structural_fingerprint():
    html = """
    <html>
      <body>
        <div class="card">
          <p></p>
          <p></p>
        </div>
      </body>
    </html>
    """
    fp = dom_structure.structural_fingerprint(html)
    assert fp["schema"] == "blueprobe-dom-fingerprint/1"
    assert fp["max_depth"] >= 3
    assert fp["total_nodes"] >= 4
    assert fp["tag_counts"]["p"] == 2
    assert isinstance(fp["skeleton_sha256"], str)
    assert len(fp["skeleton_sha256"]) == 64


def test_generate_random_dom_reproducible_with_seed():
    dom1 = dom_structure.generate_random_dom(depth=3, max_breadth=2, seed=42)
    dom2 = dom_structure.generate_random_dom(depth=3, max_breadth=2, seed=42)
    assert dom1 == dom2
    assert "<html>" in dom1
    assert "</html>" in dom1


def test_ingest_har():
    har_json = {
        "log": {
            "entries": [
                {
                    "request": {"url": "https://example.com/index.html"},
                    "response": {
                        "status": 200,
                        "content": {
                            "mimeType": "text/html; charset=utf-8",
                            "text": "<html><body><article class='markdown-body'><h1>Title</h1></article></body></html>",
                        },
                    },
                },
                {
                    "request": {"url": "https://example.com/api/data.json"},
                    "response": {
                        "status": 200,
                        "content": {
                            "mimeType": "application/json",
                            "text": '{"key": "value"}',
                        },
                    },
                },
            ]
        }
    }
    results = dom_structure.ingest_har(har_json)
    assert len(results) == 1
    assert results[0]["url"] == "https://example.com/index.html"
    assert results[0]["status"] == 200
    assert "Title" not in results[0]["skeleton"]
    assert "markdown-body" in results[0]["skeleton"]


def test_detect_pattern_with_skeleton():
    html_with_text = """
    <html>
      <body>
        <article class="markdown-body">
          <h1>Some Private User Content</h1>
          <p>More private content...</p>
        </article>
      </body>
    </html>
    """
    matches = dom_patterns.detect_pattern(html_with_text, use_skeleton=True)
    assert matches
    assert matches[0]["pattern"]["key"] == "github_readme"
