# arxiv-paper

arXiv の RSS から論文一覧を取得し、HTML にまとめるツールです。タイトルに含まれるキーワードに応じてラベル（タグ）を付け、一覧と詳細の両方にバッジとして表示します。
まだつくりかけなので、csCRのみで動作します。

## プログラムの概要

1. **自動取得**  
   [arXiv の RSS](https://arxiv.org/help/rss)（例: `http://arxiv.org/rss/cs.CR`）を `feedparser` で読み込み、エントリ（タイトル・著者・要約・リンクなど）を取得します。  
   取得処理は `scripts/create_daily_html.py`、HTML の組み立ては `scripts/html_content.py` です。

2. **キーワードに基づくタグ付け**  
   `scripts/keywords_config.py` の `KEYWORD_LABELS` で、ラベル名・キーワード一覧・表示色を定義しています。`find_labels()` が論文タイトルを小文字化し、いずれかのキーワードが部分一致したラベルを付与します（同一ラベルはタイトル内で複数キーワードが当たっても 1 回だけ）。  
   興味のある分野に合わせて `KEYWORD_LABELS` を編集してください。

3. **エントリポイント**  
   - `scripts/main.py` … `create_daily_html.py` を実行したあと、`site/csCR/` 内の日次 HTML を列挙して `site/index.html`（cs.CR 向けの一覧ページ）を生成します。  
   - `scripts/create_daily_html.py` … `--category` などでカテゴリを変え、`site/<カテゴリ名>/`（例: `csCR`, `mathAG`, `statML`）に `arXiv_<カテゴリ>_<日付>_<件数>.html` を出力します。

4. **定期実行**  
   `.github/workflows/pages.yml` で `main` への push・手動実行・毎日（UTC 09:00、日本時間 18:00）に `uv run scripts/main.py` が走り、生成物を GitHub Pages 用の `site` ディレクトリとしてデプロイします。

### ローカルでの実行例

```bash
uv run scripts/main.py
```

別カテゴリのみ生成する例:

```bash
uv run scripts/create_daily_html.py --category stat.ML
```

## ディレクトリ構成

リポジトリ直下の論理的な構成です（`site` 配下には生成された HTML が多数置かれます）。

```
arxiv-paper/
├── .github/
│   └── workflows/
│       └── pages.yml          # GitHub Actions（取得・ビルド・Pages デプロイ）
├── scripts/
│   ├── main.py                # 日次 HTML 生成 → site/index.html 更新
│   ├── create_daily_html.py   # RSS 取得と HTML ファイル出力
│   ├── html_content.py        # HTML テンプレート・ラベル表示・UI 用 JS
│   └── keywords_config.py     # キーワード ↔ ラベル・色の定義
├── site/                      # 静的サイト出力先（Pages の artifact ルート）
│   ├── index.html             # main.py が生成（cs.CR 日次へのリンク集）
│   ├── csCR/                  # cs.CR 向け日次 HTML（例）
│   ├── mathAG/                # math.AG 向け（手動や別実行で生成した場合など）
│   └── statML/                # stat.ML 向け
├── pyproject.toml
├── uv.lock
├── .python-version
├── .nojekyll                  # Jekyll 無効化（GitHub Pages 用）
└── README.md
```

`.venv` はローカル開発用の仮想環境であり、リポジトリに含める必要はありません。
