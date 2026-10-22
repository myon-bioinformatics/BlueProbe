"""DOM Structure Pattern Collection & Classification Module.

Provides preset pattern definitions, categorizations, and matching helpers
for common HTML/DOM page layouts (e.g., GitHub README, Reader View, Documentation,
Portfolio/Profile sections, NPB tables, Generic Main).

Allows selecting CSS extraction selectors via dropdown choices or preset keys
rather than manually entering CSS rules.
"""
from __future__ import annotations

try:
    from selectolax.lexbor import LexborHTMLParser as HTMLParser
except ImportError:
    from selectolax.parser import HTMLParser

SCHEMA = "blueprobe-dom-patterns/1"

CATEGORIES = [
    {"key": "repository_readme", "label": "リポジトリ README / Markdown プレビュー"},
    {"key": "developer_git", "label": "開発者・Git・Q&A プラットフォーム (GitLab / StackOverflow / npm / PyPI)"},
    {"key": "tech_publishing", "label": "技術ニュース・記事投稿メディア (HackerNews / Dev.to / Zenn / Qiita / Medium)"},
    {"key": "social_media", "label": "SNS・ソーシャルメディア (X/Twitter / Reddit / Mastodon / Bluesky / Discord)"},
    {"key": "article_reader", "label": "記事・ブログ・ニュース本文 (Article / Reader)"},
    {"key": "documentation", "label": "技術ドキュメント・解説ページ (Documentation)"},
    {"key": "portfolio_bio", "label": "ポートフォリオ・自己紹介・Profile 領域"},
    {"key": "reader_view", "label": "テキスト重視リーダービュー (Reader View)"},
    {"key": "ecommerce", "label": "Eコマース・商品詳細 (Amazon / eBay / Shopify)"},
    {"key": "search_engines", "label": "主要検索エンジン (Bing / DuckDuckGo / Yahoo!)"},
    {"key": "google_services", "label": "Google 現行サービス群 (Search / Maps / Scholar / Play / Workspace / YouTube)"},
    {"key": "google_discontinued", "label": "Google 終了サービス群 (Google+ / Reader / Wave / Allo / Orkut / Picasa)"},
    {"key": "npb_sports", "label": "NPB（プロ野球）公式日程・成績表"},
    {"key": "generic", "label": "汎用メインコンテンツ領域 (Generic Main)"},
]

DOM_PATTERNS = {
    "github_readme": {
        "key": "github_readme",
        "label": "GitHub README / Markdown Body",
        "category": "repository_readme",
        "selector": "article.markdown-body, .markdown-body",
        "description": "GitHub や Git ホスティングサービスの README プレビュー・Markdown 描画領域",
        "example_sites": ["GitHub", "Forgejo / Gitea", "npm / PyPI README"],
    },
    "article_body": {
        "key": "article_body",
        "label": "Article / Blog Main Body",
        "category": "article_reader",
        "selector": "article, [role='main'] article, .article-body, .entry-content, .post-content",
        "description": "ニュース記事・技術ブログ・メディアサイトの主要記事本文領域",
        "example_sites": ["Tech Blogs", "News Articles", "WordPress Posts"],
    },
    "documentation_main": {
        "key": "documentation_main",
        "label": "Documentation Main Section",
        "category": "documentation",
        "selector": "main, [role='main'], article.doc-content, .docs-content, .md-content",
        "description": "技術ドキュメントやライブラリ解説ページのメインコンテンツ領域",
        "example_sites": ["Read the Docs", "Docusaurus", "MkDocs", "Sphinx"],
    },
    "portfolio_profile": {
        "key": "portfolio_profile",
        "label": "Portfolio / Profile Section",
        "category": "portfolio_bio",
        "selector": "section#about, #about, .profile, .portfolio, section.bio, #portfolio",
        "description": "ポートフォリオサイトや開発者・著者の自己紹介 (About/Profile) 領域",
        "example_sites": ["Personal Portfolio", "GitHub Pages Portfolio", "Resume Sites"],
    },
    "reader_page": {
        "key": "reader_page",
        "label": "Distraction-free Reader View",
        "category": "reader_view",
        "selector": "#reader-content, .reader-view, article, main",
        "description": "リーダーモードやノイズを除去したテキスト閲覧領域",
        "example_sites": ["Reader View", "Web Clipper", "Simplified Article"],
    },
    "npb_calendar": {
        "key": "npb_calendar",
        "label": "NPB Schedule Calendar Table",
        "category": "npb_sports",
        "selector": "#calendar, .calendar, table.calendar",
        "description": "プロ野球（NPB）公式戦の月別・チーム別日程カレンダー表",
        "example_sites": ["npb.jp bis calendar"],
    },
    "npb_linescore": {
        "key": "npb_linescore",
        "label": "NPB Game Linescore Table",
        "category": "npb_sports",
        "selector": "table.score_table, .linescore, #linescore",
        "description": "プロ野球（NPB）試合ページの得点表（ラン・ヒット・エラー）",
        "example_sites": ["npb.jp linescore"],
    },
    "google_search": {
        "key": "google_search",
        "label": "Google Search Results Layout",
        "category": "google_services",
        "selector": "#search, .g, #rso, div[data-async-context]",
        "description": "Google Web 検索結果画面のコンテナおよび結果エントリー領域",
        "example_sites": ["Google Search"],
    },
    "google_scholar": {
        "key": "google_scholar",
        "label": "Google Scholar Results Layout",
        "category": "google_services",
        "selector": ".gs_r, #gs_res_ccl, .gs_ri",
        "description": "Google Scholar 学術論文検索結果リストおよびコンテナ領域",
        "example_sites": ["Google Scholar"],
    },
    "google_play": {
        "key": "google_play",
        "label": "Google Play Store Page Layout",
        "category": "google_services",
        "selector": ".VfPpkd-Wsjh2c, .fL83ws, [role='main']",
        "description": "Google Play アプリ・コンテンツ詳細画面のコンテナ領域",
        "example_sites": ["Google Play Store"],
    },
    "google_workspace_doc": {
        "key": "google_workspace_doc",
        "label": "Google Workspace / Docs Canvas Layout",
        "category": "google_services",
        "selector": ".kix-appview, .docs-editor, #docs-chrome",
        "description": "Google Docs / Workspace エディタおよびドキュメント表示領域",
        "example_sites": ["Google Docs / Sheets / Slides"],
    },
    "google_maps": {
        "key": "google_maps",
        "label": "Google Maps Web App Layout",
        "category": "google_services",
        "selector": "#scene, #content-container, .widget-scene, #searchbox",
        "description": "Google Maps Web アプリケーションのマップビュー・検索ボックス・情報パネル領域",
        "example_sites": ["Google Maps"],
    },
    "google_youtube": {
        "key": "google_youtube",
        "label": "Google YouTube Page Layout",
        "category": "google_services",
        "selector": "ytd-app, #primary, #contents, ytd-watch-flexy",
        "description": "YouTube アプリケーションコンテナ・動画視聴・動画一覧領域",
        "example_sites": ["YouTube"],
    },
    "google_plus": {
        "key": "google_plus",
        "label": "Google+ Legacy SNS Stream Layout",
        "category": "google_discontinued",
        "selector": "[data-group-id], .c-b-p-R, .yAa, .u8b",
        "description": "Google+ (サ終) のタイムラインストリーム・ポスト・コミュニティカード領域",
        "example_sites": ["Google+ (Discontinued)"],
    },
    "google_reader": {
        "key": "google_reader",
        "label": "Google Reader RSS Feed Layout",
        "category": "google_discontinued",
        "selector": "#entries, .entry, #viewer-container, #nav",
        "description": "Google Reader (サ終) の RSS フィードエントリーリスト・閲覧パネル領域",
        "example_sites": ["Google Reader (Discontinued)"],
    },
    "google_wave": {
        "key": "google_wave",
        "label": "Google Wave Workspace Layout",
        "category": "google_discontinued",
        "selector": ".wave-panel, .wave-root, .wave-gadget",
        "description": "Google Wave (サ終) のリアルタイム協調編集パネル・ウェーブコンテナ領域",
        "example_sites": ["Google Wave (Discontinued)"],
    },
    "google_allo_web": {
        "key": "google_allo_web",
        "label": "Google Allo Web Messenger Layout",
        "category": "google_discontinued",
        "selector": ".conversation-container, .message-list",
        "description": "Google Allo Web (サ終) のチャットスレッド・メッセージリスト領域",
        "example_sites": ["Google Allo Web (Discontinued)"],
    },
    "google_orkut": {
        "key": "google_orkut",
        "label": "Google Orkut Social Network Layout",
        "category": "google_discontinued",
        "selector": ".orkut-body, #profile-container, .scrapbook",
        "description": "Orkut (サ終) のソーシャルプロファイル・スクラップブック領域",
        "example_sites": ["Orkut (Discontinued)"],
    },
    "google_picasa": {
        "key": "google_picasa",
        "label": "Google Picasa Web Albums Layout",
        "category": "google_discontinued",
        "selector": ".gphoto-album, .picasa-photo-grid, #album-view",
        "description": "Picasa Web Albums (サ終) のフォトアルバム・写真グリッド領域",
        "example_sites": ["Picasa Web Albums (Discontinued)"],
    },
    "gitlab_readme": {
        "key": "gitlab_readme",
        "label": "GitLab README / Blob Viewer Layout",
        "category": "developer_git",
        "selector": "article.file-content, .readme-holder, .blob-viewer",
        "description": "GitLab のリポジトリ README およびコードビューア領域",
        "example_sites": ["GitLab"],
    },
    "bitbucket_readme": {
        "key": "bitbucket_readme",
        "label": "Bitbucket Repository README Layout",
        "category": "developer_git",
        "selector": ".bitbucket-readme, #readme, .readme-content",
        "description": "Bitbucket リポジトリの README 描画領域",
        "example_sites": ["Bitbucket"],
    },
    "stackoverflow_qa": {
        "key": "stackoverflow_qa",
        "label": "Stack Overflow / Q&A Post Layout",
        "category": "developer_git",
        "selector": "#answers, .question, .answer, .post-text, .js-post-body",
        "description": "Stack Overflow や Q&A サイトの質問・回答本文領域",
        "example_sites": ["Stack Overflow", "Stack Exchange"],
    },
    "pypi_readme": {
        "key": "pypi_readme",
        "label": "PyPI Package Description Layout",
        "category": "developer_git",
        "selector": "#description, .project-description, .article",
        "description": "PyPI (Python Package Index) パッケージ解説ページ本文領域",
        "example_sites": ["PyPI"],
    },
    "npm_readme": {
        "key": "npm_readme",
        "label": "npm Package README Layout",
        "category": "developer_git",
        "selector": "#readme, article._7823f6e9, article.markdown",
        "description": "npm パッケージ詳細ページの README 描画領域",
        "example_sites": ["npm"],
    },
    "x_twitter_timeline": {
        "key": "x_twitter_timeline",
        "label": "X / Twitter Timeline & Tweet Layout",
        "category": "social_media",
        "selector": "[data-testid='tweet'], [data-testid='primaryColumn'], [role='region']",
        "description": "X (旧 Twitter) のタイムライン・ツイートポスト領域",
        "example_sites": ["X (Twitter)"],
    },
    "reddit_thread": {
        "key": "reddit_thread",
        "label": "Reddit Post & Thread Layout",
        "category": "social_media",
        "selector": "sharded-scroller, [data-testid='post-container'], .Post, [shreddit-post]",
        "description": "Reddit の投稿スレッド・スレッドコメント領域",
        "example_sites": ["Reddit"],
    },
    "mastodon_status": {
        "key": "mastodon_status",
        "label": "Mastodon / ActivityPub Status Layout",
        "category": "social_media",
        "selector": ".status__content, .entry, .status",
        "description": "Mastodon などの分散 SNS (ActivityPub) のトゥート・ステータス領域",
        "example_sites": ["Mastodon"],
    },
    "bluesky_post": {
        "key": "bluesky_post",
        "label": "Bluesky Feed & Post Layout",
        "category": "social_media",
        "selector": "[data-testid='postThread'], [data-testid='feedItem']",
        "description": "Bluesky のフィードおよびポストスレッド領域",
        "example_sites": ["Bluesky"],
    },
    "discord_web": {
        "key": "discord_web",
        "label": "Discord Web Chat Container",
        "category": "social_media",
        "selector": "[class*='messagesWrapper'], [class*='chatContent'], [role='log']",
        "description": "Discord Web 版のチャットメッセージ・ログ領域",
        "example_sites": ["Discord Web"],
    },
    "hacker_news": {
        "key": "hacker_news",
        "label": "Hacker News Story & Comment Layout",
        "category": "tech_publishing",
        "selector": "table.fatitem, table.itemList, .comment-tree",
        "description": "Hacker News のニュースリスト・コメントツリー領域",
        "example_sites": ["Hacker News"],
    },
    "devto_article": {
        "key": "devto_article",
        "label": "Dev.to Tech Article Layout",
        "category": "tech_publishing",
        "selector": "#article-show-container, .crayons-article__main",
        "description": "Dev.to 技術記事のメイン本文領域",
        "example_sites": ["Dev.to"],
    },
    "zenn_article": {
        "key": "zenn_article",
        "label": "Zenn Tech Article Layout",
        "category": "tech_publishing",
        "selector": ".zn-topic-content, .zn-styled-body, article",
        "description": "Zenn.dev の技術記事本文領域",
        "example_sites": ["Zenn.dev"],
    },
    "qiita_article": {
        "key": "qiita_article",
        "label": "Qiita Tech Article Layout",
        "category": "tech_publishing",
        "selector": ".p-hyuki, [data-hyperion-target='body'], article",
        "description": "Qiita の技術記事本文領域",
        "example_sites": ["Qiita"],
    },
    "medium_article": {
        "key": "medium_article",
        "label": "Medium Article Body Layout",
        "category": "tech_publishing",
        "selector": "article, section[data-field='body'], .postArticle-content",
        "description": "Medium の記事本文描画領域",
        "example_sites": ["Medium"],
    },
    "amazon_product": {
        "key": "amazon_product",
        "label": "Amazon Product Detail Layout",
        "category": "ecommerce",
        "selector": "#dp-container, #productTitle, #centerCol",
        "description": "Amazon 商品詳細ページのコンテナ領域",
        "example_sites": ["Amazon"],
    },
    "ebay_item": {
        "key": "ebay_item",
        "label": "eBay Item Listing Layout",
        "category": "ecommerce",
        "selector": "#mainContent, .x-item-title, .x-item-card",
        "description": "eBay 商品ページおよびカード領域",
        "example_sites": ["eBay"],
    },
    "shopify_product": {
        "key": "shopify_product",
        "label": "Shopify Product Page Layout",
        "category": "ecommerce",
        "selector": ".product-single, .product-template, [data-product-single]",
        "description": "Shopify ストアの商品詳細コンテナ領域",
        "example_sites": ["Shopify Stores"],
    },
    "bing_search": {
        "key": "bing_search",
        "label": "Bing Search Results Layout",
        "category": "search_engines",
        "selector": "#b_results, .b_algo, #b_content",
        "description": "Microsoft Bing 検索結果リストコンテナ領域",
        "example_sites": ["Microsoft Bing"],
    },
    "duckduckgo_search": {
        "key": "duckduckgo_search",
        "label": "DuckDuckGo Search Results Layout",
        "category": "search_engines",
        "selector": "#links, .react-results--main, .result",
        "description": "DuckDuckGo 検索結果リスト領域",
        "example_sites": ["DuckDuckGo"],
    },
    "yahoo_search": {
        "key": "yahoo_search",
        "label": "Yahoo! Search Results Layout",
        "category": "search_engines",
        "selector": "#main, .web-result, #web",
        "description": "Yahoo! 検索結果リストコンテナ領域",
        "example_sites": ["Yahoo! Search"],
    },
    "generic_main": {
        "key": "generic_main",
        "label": "Generic Main Region",
        "category": "generic",
        "selector": "main, #main, #content, .main-content",
        "description": "HTML5 標準の main タグおよび一般的な主要コンテンツ領域",
        "example_sites": ["Generic Web Pages"],
    },
}


def list_patterns() -> list[dict]:
    """Return all pattern metadata dicts for dropdown UI choices or CLI selection."""
    return [dict(p) for p in DOM_PATTERNS.values()]


def list_categories() -> list[dict]:
    """Return category options."""
    return [dict(c) for c in CATEGORIES]


def get_pattern(pattern_key: str) -> dict:
    """Retrieve pattern metadata dict by key or alias.

    Raises ValueError if pattern_key is unknown.
    """
    if not isinstance(pattern_key, str) or not pattern_key.strip():
        raise ValueError("pattern_key must be a non-empty string")
    key = pattern_key.strip().lower()
    if key not in DOM_PATTERNS:
        valid_keys = ", ".join(sorted(DOM_PATTERNS.keys()))
        raise ValueError(f"unknown pattern key {pattern_key!r}. Valid keys: {valid_keys}")
    return dict(DOM_PATTERNS[key])


def get_selector_for_pattern(pattern_key: str) -> str:
    """Get the CSS selector corresponding to a pattern key."""
    return get_pattern(pattern_key)["selector"]


def detect_pattern(html: str, *, use_skeleton: bool = True) -> list[dict]:
    """Analyze DOM HTML (or its structural skeleton) and return candidate pattern matches ranked by match score.

    Score is based on selector presence and node matching count.
    Returns list of dicts:
      [{"pattern": pattern_dict, "score": int, "matched_nodes": int, "selector_used": str}, ...]
    """
    if not isinstance(html, str) or not html.strip():
        return []
    if use_skeleton:
        from dom_structure import skeletonize
        html = skeletonize(html)
    tree = HTMLParser(html)
    results = []
    for pattern in DOM_PATTERNS.values():
        selector = pattern["selector"]
        sub_selectors = [s.strip() for s in selector.split(",") if s.strip()]
        total_matched = 0
        best_sub_selector = None
        for sub in sub_selectors:
            try:
                nodes = tree.css(sub)
                if nodes:
                    count = len(nodes)
                    total_matched += count
                    if best_sub_selector is None:
                        best_sub_selector = sub
            except Exception:
                continue
        if total_matched > 0:
            # Score gives preference to specific selectors (e.g. github_readme) over broad ones (e.g. generic_main)
            specificity_bonus = 10 if pattern["key"] not in ("generic_main", "reader_page") else 2
            score = total_matched + specificity_bonus
            results.append({
                "pattern": dict(pattern),
                "score": score,
                "matched_nodes": total_matched,
                "selector_used": best_sub_selector or selector,
            })
    results.sort(key=lambda r: (r["score"], r["matched_nodes"]), reverse=True)
    return results
