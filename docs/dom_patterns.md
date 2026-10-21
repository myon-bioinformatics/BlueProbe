# DOM 構造パターン・プリセット設計 (`dom_patterns.py`)

BlueProbe は保存済み HTML の DOM 構造から特定の主要コンテンツを抽出する際、CSS セレクタを直接指定する代わりに、
ドロップダウン/プリセット指定可能な DOM パターン識別子（`github_readme` や `portfolio_profile` 等）を選択・分類できるようにしています。

## 定義されている DOM パターン一覧

| パターンキー (`key`) | カテゴリ | ラベル | CSS セレクタ (`selector`) | 対象の例 |
|---|---|---|---|---|
| `github_readme` | `repository_readme` | GitHub README / Markdown Body | `article.markdown-body, .markdown-body` | GitHub, Gitea, npm README |
| `article_body` | `article_reader` | Article / Blog Main Body | `article, [role='main'] article, .article-body, .entry-content, .post-content` | ブログ・ニュース記事本文 |
| `documentation_main` | `documentation` | Documentation Main Section | `main, [role='main'], article.doc-content, .docs-content, .md-content` | Read the Docs, Docusaurus |
| `portfolio_profile` | `portfolio_bio` | Portfolio / Profile Section | `section#about, #about, .profile, .portfolio, section.bio, #portfolio` | ポートフォリオ・自己紹介 |
| `reader_page` | `reader_view` | Distraction-free Reader View | `#reader-content, .reader-view, article, main` | リーダーモード・Web クリップ |
| `google_search` | `google_services` | Google Search Results Layout | `#search, .g, #rso, div[data-async-context]` | Google 検索結果リスト |
| `google_scholar` | `google_services` | Google Scholar Results Layout | `.gs_r, #gs_res_ccl, .gs_ri` | Google Scholar 学術検索 |
| `google_play` | `google_services` | Google Play Store Page Layout | `.VfPpkd-Wsjh2c, .fL83ws, [role='main']` | Google Play アプリ詳細 |
| `google_workspace_doc` | `google_services` | Google Workspace Canvas Layout | `.kix-appview, .docs-editor, #docs-chrome` | Google Docs / Workspace |
| `google_maps` | `google_services` | Google Maps Web App Layout | `#scene, #content-container, .widget-scene, #searchbox` | Google Maps マップ情報画面 |
| `google_youtube` | `google_services` | Google YouTube Page Layout | `ytd-app, #primary, #contents, ytd-watch-flexy` | YouTube アプリ／動画画面 |
| `google_plus` | `google_discontinued` | Google+ Stream Layout | `[data-group-id], .c-b-p-R, .yAa, .u8b` | Google+ (サ終) ストリーム |
| `google_reader` | `google_discontinued` | Google Reader Feed Layout | `#entries, .entry, #viewer-container, #nav` | Google Reader (サ終) フィード |
| `google_wave` | `google_discontinued` | Google Wave Workspace Layout | `.wave-panel, .wave-root, .wave-gadget` | Google Wave (サ終) 協調編集 |
| `google_allo_web` | `google_discontinued` | Google Allo Web Messenger Layout | `.conversation-container, .message-list` | Google Allo Web (サ終) |
| `google_orkut` | `google_discontinued` | Orkut Social Network Layout | `.orkut-body, #profile-container, .scrapbook` | Orkut (サ終) SNS |
| `google_picasa` | `google_discontinued` | Picasa Web Albums Layout | `.gphoto-album, .picasa-photo-grid, #album-view` | Picasa Web Albums (サ終) |
| `npb_calendar` | `npb_sports` | NPB Schedule Calendar Table | `#calendar, .calendar, table.calendar` | NPB 公式戦カレンダー表 |
| `npb_linescore` | `npb_sports` | NPB Game Linescore Table | `table.score_table, .linescore, #linescore` | NPB 試合得点表 |
| `generic_main` | `generic` | Generic Main Region | `main, #main, #content, .main-content` | 一般 Web ページの main |

## 使い方

### Python コードでプリセット指定する (`HtmlSource`)

```python
from html_source import HtmlSource

# パターンキーで指定 (selector は自動設定されます)
source = HtmlSource(pattern="github_readme")
report = source.parse(html, url)
```

### 自動パターン判定機能 (`detect_pattern`)

DOM 構造を解析し、マッチするパターンを候補順（スコア順）で返します。

```python
import dom_patterns

matches = dom_patterns.detect_pattern(html)
if matches:
    top_pattern = matches[0]["pattern"]
    print(f"判定されたパターン: {top_pattern['key']} ({top_pattern['label']})")
```

### CLI から一覧と指定を実行する

```bash
# 利用可能なパターン一覧を表示
uv run python blueprobe.py --list-patterns

# 特定のパターンプリセットを指定して再解析を実行
uv run python blueprobe.py --source html_source --pattern github_readme --cache <QueRyuのキャッシュ>
```
