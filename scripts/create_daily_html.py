import feedparser
from pathlib import Path
from datetime import datetime
from typing import Optional
from html_content import generate_html_content


def save_paper_list_to_html(
    category: str = "cs.CR",
    feed_url: str = "http://arxiv.org/rss/cs.CR",
    max_papers: Optional[int] = None,
    output_dir: str = "results_html",
):
    """
    arXivのRSSフィードから論文一覧を取得してHTML形式で保存する

    Args:
        feed_url: arXivのRSSフィードURL（デフォルトはcs.CR（暗号学・セキュリティ））
        max_papers: 表示する最大論文数（Noneの場合は全て表示）
        output_dir: 出力先ディレクトリ（デフォルトはresults_html）

    論文が0件のときは HTML を生成・保存しない。
    """
    print(f"arXiv RSSフィードを取得中: {feed_url}\n")

    # RSSフィードを取得
    feed = feedparser.parse(feed_url)

    if feed.bozo:
        print(f"エラー: RSSフィードの取得に失敗しました")
        if hasattr(feed, 'bozo_exception'):
            print(f"詳細: {feed.bozo_exception}")
        return

    # 論文エントリを取得
    entries = feed.entries

    # 最大論文数の制限
    if max_papers is not None:
        entries = entries[:max_papers]

    if len(entries) == 0:
        print("論文が0件のため、HTML の生成・保存をスキップします。")
        return

    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    # フィード情報を取得（エスケープ処理）
    feed_title = feed.feed.get('title', 'N/A').replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    feed_updated = feed.feed.get('updated', 'N/A')

    # HTMLコンテンツを生成
    html_content = generate_html_content(feed_title, feed_updated, entries)

    # HTMLファイルを保存
    filename = f"arXiv_{category.replace('.', '')}_{datetime.now().strftime('%Y%m%d')}_{len(entries)}.html"
    filepath = output_path / filename
    filepath.write_text(html_content, encoding='utf-8')

    print(f"HTMLファイルを保存しました: {filepath}")
    print(f"論文数: {len(entries)}件")


def main():
    """メイン関数"""
    import argparse

    parser = argparse.ArgumentParser(description='arXiv論文一覧をHTML形式で取得')
    parser.add_argument('--category', '-c', type=str, default='cs.CR',
                        help='カテゴリ（デフォルト: cs.CR）')  # math.AG, stat.ML
    parser.add_argument('--max-papers', '-m', type=int, default=None,
                        help='最大論文数（デフォルト: 全て）')
    parser.add_argument('--output-dir', '-o', type=str, default='../site/results_html',
                        help='出力先ディレクトリ（デフォルト: results_html）')

    args = parser.parse_args()

    # フィードURLを構築
    if args.category == 'all':
        feed_url = "http://arxiv.org/rss/all"
    else:
        feed_url = f"http://arxiv.org/rss/{args.category}"

    # HTML形式で保存
    save_paper_list_to_html(
        category=args.category,
        feed_url=feed_url,
        max_papers=args.max_papers,
        output_dir=f'../site/{args.category.replace(".", "")}',
    )

    # example:
    # uv run python scripts/main_rss.py  # デフォルト（cs.CR、全ての論文）
    # uv run python scripts/main_rss.py --category cs.AI --max-papers 50  # AI分野の最新50件


if __name__ == "__main__":
    main()
