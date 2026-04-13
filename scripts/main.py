"""
1 create_daily_html.py を cs.CR / stat.ML / math.AG で実行
2 site/index.html をカテゴリハブにし、各 site/<subdir>/index.html に日次一覧を書く
"""

from __future__ import annotations

import re
import subprocess
import sys
from html import escape
from pathlib import Path
from typing import NamedTuple


class CategorySpec(NamedTuple):
    arxiv_id: str
    site_subdir: str
    title: str
    description: str


_ARXIV_DAILY = re.compile(r"arXiv_.+_(\d{8})_(\d+)\.html$")

CATEGORIES: tuple[CategorySpec, ...] = (
    CategorySpec("cs.CR", "csCR", "cs.CR", "暗号・セキュリティ"),
    CategorySpec("stat.ML", "statML", "stat.ML", "機械学習（統計）"),
    CategorySpec("math.AG", "mathAG", "math.AG", "代数幾何"),
)

SCRIPTS_DIR = Path(__file__).resolve().parent
SITE_DIR = SCRIPTS_DIR.parent / "site"
INDEX_PATH = SITE_DIR / "index.html"
CREATE_DAILY = SCRIPTS_DIR / "create_daily_html.py"

_STYLES = """
body{font-family:system-ui,-apple-system,sans-serif;line-height:1.6;color:#333;max-width:960px;margin:0 auto;padding:24px;background:#f5f5f5}
h1{color:#2c3e50;border-bottom:3px solid #3498db;padding-bottom:10px}
.panel{background:#fff;border-radius:8px;padding:20px 24px;box-shadow:0 2px 4px rgba(0,0,0,.08)}
ul{list-style:none;padding:0;margin:0}
li{padding:10px 0;border-bottom:1px solid #ecf0f1}
li:last-child{border-bottom:none}
a{color:#2980b9;text-decoration:none}a:hover{text-decoration:underline}
.meta{color:#7f8c8d;font-size:.9em;margin-top:16px}
.hub-card{display:block;padding:16px 20px;margin-bottom:12px;background:#fff;border-radius:8px;box-shadow:0 2px 4px rgba(0,0,0,.08);border-left:4px solid #3498db}
.hub-card:hover{box-shadow:0 4px 8px rgba(0,0,0,.12)}
.hub-card strong{font-size:1.15em;color:#2c3e50}
.hub-card span{display:block;color:#7f8c8d;font-size:.95em;margin-top:4px}
.back{margin-bottom:20px}
"""


def _daily_label(path: Path) -> str:
    m = _ARXIV_DAILY.match(path.name)
    return f"{m.group(1)}: {m.group(2)}" if m else path.stem


def _page(title: str, inner: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>{_STYLES}</style>
</head>
<body>
{inner}
</body>
</html>
"""


def run_create_daily_html(arxiv_category: str) -> None:
    subprocess.run(
        [sys.executable, str(CREATE_DAILY), "--category", arxiv_category],
        cwd=str(SCRIPTS_DIR),
        check=True,
    )


def run_all_categories() -> None:
    for spec in CATEGORIES:
        print(f"\n--- {spec.arxiv_id} を取得します ---\n")
        run_create_daily_html(spec.arxiv_id)


def build_hub_index_html() -> str:
    cards = "\n".join(
        f'        <a class="hub-card" href="{escape(s.site_subdir)}/index.html">'
        f"<strong>{escape(s.title)}</strong><span>{escape(s.description)}</span></a>"
        for s in CATEGORIES
    )
    inner = f"""    <h1>arXiv paper list</h1>
    <p>閲覧するカテゴリを選んでください。</p>
    <div class="panel" style="padding:16px 20px;">
{cards}
    </div>
    <p class="meta">カテゴリ数: {len(CATEGORIES)}</p>"""
    return _page("arXiv 日次レポート（カテゴリ選択）", inner)


def build_category_list_html(spec: CategorySpec) -> str:
    d = SITE_DIR / spec.site_subdir
    d.mkdir(parents=True, exist_ok=True)
    files = sorted(d.glob("arXiv_*.html"), key=lambda p: p.name, reverse=True)
    if files:
        lis = "\n".join(
            f'        <li><a href="{escape(p.name)}">{escape(_daily_label(p))}</a></li>' for p in files
        )
    else:
        lis = "        <li>（まだ HTML がありません）</li>"
    inner = f"""    <p class="back"><a href="../index.html">← カテゴリ選択に戻る</a></p>
    <h1>arXiv {escape(spec.title)} papers</h1>
    <div class="panel">
        <ul>
{lis}
        </ul>
    </div>
    <p class="meta">件数: {len(files)}</p>"""
    return _page(f"arXiv {escape(spec.title)} 日次一覧", inner)


def write_hub_index_html() -> None:
    INDEX_PATH.write_text(build_hub_index_html(), encoding="utf-8")
    print(f"ハブ index を更新しました: {INDEX_PATH}")


def write_category_list_pages() -> None:
    for spec in CATEGORIES:
        out = SITE_DIR / spec.site_subdir / "index.html"
        out.write_text(build_category_list_html(spec), encoding="utf-8")
        print(f"一覧を更新しました: {out}")


def main() -> None:
    run_all_categories()
    write_hub_index_html()
    write_category_list_pages()


if __name__ == "__main__":
    main()
