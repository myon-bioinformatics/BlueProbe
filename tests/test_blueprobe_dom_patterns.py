import pytest

import dom_patterns
from html_source import HtmlSource


def test_list_patterns_and_categories_structure():
    patterns = dom_patterns.list_patterns()
    assert isinstance(patterns, list)
    assert len(patterns) >= 8
    keys = [p["key"] for p in patterns]
    assert "github_readme" in keys
    assert "article_body" in keys
    assert "documentation_main" in keys
    assert "portfolio_profile" in keys
    assert "reader_page" in keys
    assert "npb_calendar" in keys
    assert "npb_linescore" in keys
    assert "generic_main" in keys

    for p in patterns:
        assert set(p.keys()) >= {"key", "label", "category", "selector", "description", "example_sites"}

    categories = dom_patterns.list_categories()
    cat_keys = [c["key"] for c in categories]
    assert "repository_readme" in cat_keys
    assert "portfolio_bio" in cat_keys


def test_get_pattern_valid_and_invalid():
    readme_pattern = dom_patterns.get_pattern("github_readme")
    assert readme_pattern["key"] == "github_readme"
    assert readme_pattern["category"] == "repository_readme"
    assert readme_pattern["selector"] == "article.markdown-body, .markdown-body"

    portfolio_pattern = dom_patterns.get_pattern("PORTFOLIO_PROFILE")
    assert portfolio_pattern["key"] == "portfolio_profile"

    with pytest.raises(ValueError, match="unknown pattern key"):
        dom_patterns.get_pattern("invalid_pattern_xyz")

    with pytest.raises(ValueError, match="must be a non-empty string"):
        dom_patterns.get_pattern("")


def test_html_source_initialization_with_pattern():
    source = HtmlSource(pattern="github_readme")
    assert source.pattern == "github_readme"
    assert source.selector == "article.markdown-body, .markdown-body"

    override_source = HtmlSource(pattern="github_readme", selector="main")
    assert override_source.pattern == "github_readme"
    assert override_source.selector == "main"


def test_detect_pattern_classifies_github_readme():
    html = """
    <html>
      <body>
        <header>Header</header>
        <article class="markdown-body">
          <h1>Project Title</h1>
          <p>Description text for repo</p>
        </article>
      </body>
    </html>
    """
    matches = dom_patterns.detect_pattern(html)
    assert matches
    top_match = matches[0]
    assert top_match["pattern"]["key"] == "github_readme"
    assert top_match["matched_nodes"] >= 1


def test_detect_pattern_classifies_portfolio_profile():
    html = """
    <html>
      <body>
        <nav>Navigation</nav>
        <section id="about" class="profile">
          <h2>About Me</h2>
          <p>Software Engineer & Portfolio Bio</p>
        </section>
      </body>
    </html>
    """
    matches = dom_patterns.detect_pattern(html)
    assert matches
    top_match = matches[0]
    assert top_match["pattern"]["key"] == "portfolio_profile"


def test_detect_pattern_classifies_documentation_main():
    html = """
    <html>
      <body>
        <aside>Sidebar</aside>
        <main class="docs-content">
          <h1>API Documentation</h1>
          <p>Endpoints and guide</p>
        </main>
      </body>
    </html>
    """
    matches = dom_patterns.detect_pattern(html)
    assert matches
    top_match = matches[0]
    assert top_match["pattern"]["key"] == "documentation_main"


def test_detect_pattern_empty_or_no_match():
    assert dom_patterns.detect_pattern("") == []
    assert dom_patterns.detect_pattern("   ") == []

    no_match_html = "<div><span>Just a simple div</span></div>"
    matches = dom_patterns.detect_pattern(no_match_html)
    # Simple div shouldn't match specialized selectors like github_readme or portfolio_profile
    keys = [m["pattern"]["key"] for m in matches]
    assert "github_readme" not in keys
    assert "portfolio_profile" not in keys


def test_google_services_pattern_presets():
    # Verify google_services category and pattern keys exist
    search_pattern = dom_patterns.get_pattern("google_search")
    assert search_pattern["category"] == "google_services"

    doc_pattern = dom_patterns.get_pattern("google_workspace_doc")
    assert doc_pattern["key"] == "google_workspace_doc"

    maps_pattern = dom_patterns.get_pattern("google_maps")
    assert maps_pattern["category"] == "google_services"

    # Test Google Search classification
    google_search_html = "<html><body><div id='search'><div class='g'>Result 1</div></div></body></html>"
    search_matches = dom_patterns.detect_pattern(google_search_html)
    assert search_matches
    assert search_matches[0]["pattern"]["key"] == "google_search"

    # Test YouTube classification
    youtube_html = "<html><body><ytd-app><div id='primary'>Player</div></ytd-app></body></html>"
    yt_matches = dom_patterns.detect_pattern(youtube_html)
    assert yt_matches
    assert yt_matches[0]["pattern"]["key"] == "google_youtube"


def test_google_discontinued_services_pattern_presets():
    reader_pattern = dom_patterns.get_pattern("google_reader")
    assert reader_pattern["category"] == "google_discontinued"

    plus_pattern = dom_patterns.get_pattern("google_plus")
    assert plus_pattern["category"] == "google_discontinued"

    # Test Google Reader pattern match
    reader_html = "<html><body><div id='entries'><div class='entry'>Item</div></div></body></html>"
    reader_matches = dom_patterns.detect_pattern(reader_html)
    assert reader_matches
    assert reader_matches[0]["pattern"]["key"] == "google_reader"
