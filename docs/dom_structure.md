# DOM 構造スケルトン化・集約・合成・HAR アーカイブ取り込み (`dom_structure.py`)

BlueProbe では、特定のWebサイト（プロ野球等）に依存しない汎用的な DOM 構造の把握・集約のために、
**本文テキスト（記事本文・見出し文等）を一切保持せず、純粋な HTML タグ階層構造 (`<html>`〜`</html>`) と属性構造のみ**を抽出・観測する機能を提供しています。

本文テキストを保持しないことで、文章の著作権・権利上の懸念を排除しつつ、HTML DOM 構造のトポロジー（深さ・要素分布・コンテナパターン）のみを集積・解析できます。

## 主な機能

### 1. 構造スケルトン化 (`skeletonize`)

テキストノード、`<script>`、`<style>` の中身を除去し、タグの入れ子構造と構造属性 (`id`, `class`, `role`, `type` 等) のみを残します。

```python
import dom_structure

raw_html = "<html><body><main class='content'><h1>タイトル</h1><p>本文テキスト</p></main></body></html>"
skeleton = dom_structure.skeletonize(raw_html)
# 結果: <html><body><main class="content"><h1></h1><p></p></main></body></html>
```

### 2. 構造フィンガープリント計算 (`structural_fingerprint`)

DOM ツリーの最大深さ、要素数、タグ分布、スケルトンの SHA-256 ハッシュ、構造シグネチャを算出します。

```python
fp = dom_structure.structural_fingerprint(html)
# {
#   "schema": "blueprobe-dom-fingerprint/1",
#   "max_depth": 4,
#   "total_nodes": 12,
#   "tag_counts": {"div": 4, "p": 3, "a": 2, ...},
#   "skeleton_sha256": "...",
#   "structural_signature": "d4_n12[div:4,p:3,a:2]"
# }
```

### 3. 合成ランダム DOM 構造生成 (`generate_random_dom`)

多様な DOM ツリー構造を合成・疑似生成し、パターン判定やストレステストに利用します（`seed` 指定で再現可能）。

```python
random_html = dom_structure.generate_random_dom(depth=4, max_breadth=3, seed=42)
```

### 4. HAR (HTTP Archive) アライアンス／アーカイブの取り込み (`ingest_har`)

ブラウザやプロキシから出力される HAR ファイル (`.har`) から HTML 応答を抽出し、一括で構造スケルトン化・フィンガープリント抽出を行います。

```python
results = dom_structure.ingest_har(har_json_data)
```

```bash
# CLI から HAR ファイルを取り込んで構造スケルトンを出力
uv run python blueprobe.py --har archive.har --out skeletons.json
```
