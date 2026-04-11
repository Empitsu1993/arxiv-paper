"""
1 create_daily_html.py を実行して日次 HTML を生成する
2 site/index.html を csCR 配下の一覧ページとして書き出す
"""

from __future__ import annotations

import re
import subprocess
import sys
from html import escape
from pathlib import Path


# create_daily_html の出力: arXiv_csCR_YYYYMMDD_N.html（N = 論文数）
_CS_CR_LIST_LABEL = re.compile(r"arXiv_csCR_(\d{8})_(\d+)\.html$")


def _list_label_for_cs_cr_html(path: Path) -> str:
    m = _CS_CR_LIST_LABEL.match(path.name)
    if m:
        return f"{m.group(1)}_{m.group(2)}本"
    return path.stem


SCRIPTS_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPTS_DIR.parent
SITE_DIR = REPO_ROOT / "site"
CS_CR_DIR = SITE_DIR / "csCR"
INDEX_PATH = SITE_DIR / "index.html"


def run_create_daily_html() -> None:
    """scripts ディレクトリを cwd にして create_daily_html.py を実行する。"""
    script = SCRIPTS_DIR / "create_daily_html.py"
    subprocess.run(
        [sys.executable, str(script)],
        cwd=str(SCRIPTS_DIR),
        check=True,
    )


def build_index_html() -> str:
    """site/csCR 内の arXiv_*.html へのリンク一覧 HTML を返す。"""
    if not CS_CR_DIR.is_dir():
        CS_CR_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(
        CS_CR_DIR.glob("arXiv_*.html"),
        key=lambda p: p.name,
        reverse=True,
    )

    items: list[str] = []
    for p in files:
        href = f"csCR/{escape(p.name)}"
        label = escape(_list_label_for_cs_cr_html(p))
        items.append(f'        <li><a href="{href}">{label}</a></li>')

    list_body = "\n".join(items) if items else "        <li>（まだ HTML がありません）</li>"

    return f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>arXiv cs.CR papers</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 960px;
            margin: 0 auto;
            padding: 24px;
            background: #f5f5f5;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        .panel {{
            background: #fff;
            border-radius: 8px;
            padding: 20px 24px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        }}
        ul {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        li {{
            padding: 10px 0;
            border-bottom: 1px solid #ecf0f1;
        }}
        li:last-child {{ border-bottom: none; }}
        a {{ color: #2980b9; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        .meta {{ color: #7f8c8d; font-size: 0.9em; margin-top: 16px; }}
    </style>
</head>
<body>
    <h1>arXiv cs.CR 日次レポート</h1>
    <p>「論文一覧」ページ（<code>html_content</code> で生成した HTML）へのリンクです。</p>
    <div class="panel">
        <ul>
{list_body}
        </ul>
    </div>
    <p class="meta">件数: {len(files)}</p>
</body>
</html>
"""


def write_index_html() -> None:
    INDEX_PATH.write_text(build_index_html(), encoding="utf-8")
    print(f"index を更新しました: {INDEX_PATH}")


def main() -> None:
    run_create_daily_html()
    write_index_html()


if __name__ == "__main__":
    main()
